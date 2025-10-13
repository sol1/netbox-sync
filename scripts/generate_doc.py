#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_doc.py

Auto-generates Markdown documentation from ConfigBase-derived classes
(e.g. CommonConfig) that define .options using ConfigOption().

Reads from:
  - module/common/config.py
  - module/netbox/config.py

Writes to:
  - docs/dev/common_config.md
  - docs/dev/netbox_config.md
"""

import importlib.util
import inspect
import os
import re
import sys
from textwrap import dedent
from loguru import logger

# --- Add project root to sys.path so "module" imports work ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import base type to detect config classes reliably (requires ROOT_DIR on sys.path)
from module.config.base import ConfigBase

# Paths relative to project root
DOCS_DIR = os.path.join(ROOT_DIR, "docs", "config")

CONFIG_SOURCES = {
    "Common": os.path.join(ROOT_DIR, "module", "common", "config.py"),
    "Netbox": os.path.join(ROOT_DIR, "module", "netbox", "config.py"),
    "Source Redfish": os.path.join(ROOT_DIR, "module", "sources", "check_redfish", "config.py"),
    "Source VMWare": os.path.join(ROOT_DIR, "module", "sources", "vmware", "config.py"),
}


def load_module_from_path(name, path):
    """Dynamically load a module from an arbitrary file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_config_classes(module):
    """Find config section classes (subclasses of ConfigBase, excluding the base)."""
    config_classes = []
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, ConfigBase) and obj is not ConfigBase:
            config_classes.append(obj)
    return config_classes


def generate_markdown_for_class(cls, heading_name: str | None = None):
    """Generate Markdown for a single config class with TOC and subsections."""

    section = getattr(cls, "section_name", cls.__name__)
    title = heading_name or section
    lines = [f"# {title} Configuration\n"]

    # Add class docstring if present
    doc = inspect.getdoc(cls)
    if doc:
        lines.append(f"{doc}\n")

    # Attempt to instantiate the config class
    try:
        instance = cls()
    except Exception:
        return "\n".join(lines)

    # Helper: flatten ConfigOptionGroups
    def iter_options(opts):
        for item in opts:
            if hasattr(item, "options") and not hasattr(item, "key"):
                yield from getattr(item, "options", [])
            else:
                yield item

    opts = list(iter_options(getattr(instance, "options", [])))
    if not opts:
        return "\n".join(lines)

    # --- TOC ---
    lines.extend(_render_toc(opts))

    # --- Detailed option descriptions ---
    lines.extend(_render_option_details(opts))

    # --- Examples ---
    lines.extend(_render_yaml_example(section, opts))
    lines.extend(_render_ini_example(section, opts))

    return "\n".join(lines)


# ---------------------------------------------------------------------
# --- Subsection functions -------------------------------------------
# ---------------------------------------------------------------------

def _render_toc(opts):
    """Render a simple Markdown Table of Contents."""
    lines = ["## TOC\n"]
    for opt in opts:
        key = getattr(opt, "key", "<unknown>")
        anchor = key
        lines.append(f"[Option: {key}](#{anchor})")
    lines.append("[Example (YAML)](#example-yaml)")
    lines.append("[Example (INI)](#example-ini)")
    lines.append("\n## Configuration Options")  # newline
    return lines

def _render_table_section(opts):
    """Render a minimal summary table (key/type/required/default)."""
    lines = ["## Summary\n", "| Key | Type | Required | Default |", "|-----|------|-----------|----------|"]

    for opt in opts:
        key = getattr(opt, "key", "<unknown>")
        value_type = getattr(opt, "value_type", str)
        type_name = value_type.__name__ if hasattr(value_type, "__name__") else str(value_type)
        mandatory = getattr(opt, "mandatory", False)
        default_value = getattr(opt, "default_value", None)

        # Simplify default rendering
        if default_value is None:
            default_value = "null"
        elif isinstance(default_value, bool):
            default_value = "true" if default_value else "false"
        else:
            default_value = str(default_value)

        lines.append(f"| `{key}` | `{type_name}` | {'✅' if mandatory else '❌'} | `{default_value}` |")

    lines.append("")  # newline after table
    return lines


def _render_option_details(opts):
    """Render detailed sections for each option (type, default, description)."""
    lines = []
    for opt in opts:
        name = getattr(opt, "key", "<unknown>")
        value_type = getattr(opt, "value_type", str)
        type_name = value_type.__name__ if hasattr(value_type, "__name__") else str(value_type)
        default_value = getattr(opt, "default_value", None)
        example = getattr(opt, "config_example", None)
        mandatory = getattr(opt, "mandatory", False)

        desc_callable = getattr(opt, "description", None)
        if callable(desc_callable):
            desc = desc_callable()
        else:
            desc = getattr(opt, "_description", "") or getattr(opt, "description", "")
            desc = str(desc).strip() if desc else ""

        lines.append(f"### `{name}`")
        meta = f"**Type:** `{type_name}`"
        meta += "  \n**Required:** `true`" if mandatory else f"  \n**Default:** `{default_value}`"
        if example is not None and example != default_value:
            meta += f"  \n**Example:** `{example}`"
        lines.append(meta + "\n")

        if desc:
            lines.append(f"{dedent(desc).strip()}\n")

    return lines


def _render_yaml_example(section, opts):
    """Render YAML example block."""
    def yaml_value(val):
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, (int, float)):
            return str(val)
        if val is None:
            return "null"
        sval = str(val)
        return f'"{sval.replace("\\", "\\\\")}"'

    lines = ["## Example (YAML)\n", "```", f"{section}:"]
    for opt in opts:
        key = opt.key
        default_value = getattr(opt, "default_value", None)
        mandatory = getattr(opt, "mandatory", False)
        example = getattr(opt, "config_example", None)

        if default_value is not None:
            lines.append(f"  {key}: {yaml_value(default_value)}")
        elif mandatory:
            placeholder = example if example is not None else "<REQUIRED>"
            lines.append(f"  # {key}: {yaml_value(placeholder)}  # required")
        else:
            if example is not None:
                lines.append(f"  # {key}: {yaml_value(example)}  # optional")
            else:
                lines.append(f"  # {key}: null  # optional")
    lines.append("```\n")
    return lines


def _render_ini_example(section, opts):
    """Render INI example block."""
    def ini_value(val):
        if isinstance(val, bool):
            return "true" if val else "false"
        return str(val)

    lines = ["## Example (INI)\n", "```", f"[{section}]"]
    for opt in opts:
        key = opt.key
        default_value = getattr(opt, "default_value", None)
        mandatory = getattr(opt, "mandatory", False)
        example = getattr(opt, "config_example", None)

        if default_value is not None:
            lines.append(f"{key} = {ini_value(default_value)}")
        elif mandatory:
            placeholder = example if example else "<REQUIRED>"
            lines.append(f"# {key} = {placeholder}  ; required")
        else:
            if example is not None:
                lines.append(f"# {key} = {example}  ; optional")
            else:
                lines.append(f"# {key} =  ; optional")
    lines.append("```\n")
    return lines



def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for key, path in CONFIG_SOURCES.items():
        if not os.path.exists(path):
            logger.warning(f"Skipping {key} — {path} not found")
            continue

        module = load_module_from_path(f"{key}_config", path)
        classes = find_config_classes(module)
        if not classes:
            logger.info(f"No config classes found in {key}")
            continue

        # Build snake_case filename from the CONFIG_SOURCES key
        def snake_case(s: str) -> str:
            s = s.strip().lower()
            s = re.sub(r"[^a-z0-9]+", "_", s)
            s = re.sub(r"_+", "_", s)
            return s.strip("_")

        out_path = os.path.join(DOCS_DIR, f"{snake_case(key)}_config.md")
        logger.info(f"[+] Writing {out_path}")

        with open(out_path, "w", encoding="utf-8") as f:
            for cls in classes:
                f.write(generate_markdown_for_class(cls, heading_name=key))
                f.write("\n---\n")


if __name__ == "__main__":
    main()
