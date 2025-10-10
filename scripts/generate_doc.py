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
    """Generate Markdown for a single config class.

    heading_name: Optional display title for the section heading (e.g. "Common").
    If not provided, falls back to the class' section_name or class name.
    """
    lines = []
    section = getattr(cls, "section_name", cls.__name__)
    title = heading_name or section
    lines.append(f"# {title} Configuration\n")
    doc = inspect.getdoc(cls)
    if doc:
        lines.append(f"{doc}\n")

    # Try a no-arg instantiation; if that fails, skip documenting the class
    try:
        instance = cls()
    except Exception:
        return "\n".join(lines)

    # Helper to iterate options, flattening groups
    def iter_options(opts):
        for item in opts:
            # ConfigOptionGroup has an 'options' list we should expand
            if hasattr(item, "options") and not hasattr(item, "key"):
                for sub in getattr(item, "options", []):
                    yield sub
            else:
                yield item

    for opt in iter_options(getattr(instance, "options", [])):
        # ConfigOption has attributes: key, value_type, default_value, config_example, mandatory
        name = getattr(opt, "key", None) or "<unknown>"
        value_type = getattr(opt, "value_type", str)
        type_name = value_type.__name__ if hasattr(value_type, "__name__") else str(value_type)
        default_value = getattr(opt, "default_value", None)
        example = getattr(opt, "config_example", None)
        mandatory = getattr(opt, "mandatory", False)

        # Description is a method via DescriptionFormatterMixin
        desc_callable = getattr(opt, "description", None)
        if callable(desc_callable):
            desc = desc_callable()
        else:
            raw_desc = getattr(opt, "_description", "") or getattr(opt, "description", "")
            desc = str(raw_desc)
            if desc:
                desc = dedent(desc).strip()

        lines.append(f"## `{name}`")

        meta = f"**Type:** `{type_name}`"
        if mandatory:
            meta += "  \n**Required:** `true`"
        else:
            meta += f"  \n**Default:** `{default_value}`"
        if example is not None and example != default_value:
            meta += f"  \n**Example:** `{example}`"
        lines.append(meta + "\n")

        if desc:
            lines.append(f"{desc}\n")

    # --- Append Examples with default values ---

    def yaml_value(val):
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, (int, float)):
            return str(val)
        if val is None:
            return "null"
        # escape backslashes for Windows paths
        sval = str(val)
        # Quote strings to be safe
        return f'"{sval.replace("\\", "\\\\")}"'

    # YAML example
    lines.append("## Example (YAML)\n")
    lines.append("```\n")
    lines.append(f"{section}:")
    for opt in iter_options(getattr(instance, "options", [])):
        default_value = getattr(opt, "default_value", None)
        mandatory = getattr(opt, "mandatory", False)
        example = getattr(opt, "config_example", None)
        if default_value is not None:
            lines.append(f"  {opt.key}: {yaml_value(default_value)}")
        else:
            if mandatory:
                placeholder = example if example is not None else "<REQUIRED>"
                lines.append(f"  # {opt.key}: {yaml_value(placeholder)}  # required")
            else:
                if example is not None:
                    lines.append(f"  # {opt.key}: {yaml_value(example)}  # optional")
                else:
                    lines.append(f"  # {opt.key}: null  # optional")
    lines.append("```\n")

    # INI example
    lines.append("## Example (INI)\n")
    lines.append("```\n")
    lines.append(f"[{section}]")
    for opt in iter_options(getattr(instance, "options", [])):
        default_value = getattr(opt, "default_value", None)
        mandatory = getattr(opt, "mandatory", False)
        example = getattr(opt, "config_example", None)
        def ini_value(val):
            if isinstance(val, bool):
                return "true" if val else "false"
            return str(val)

        if default_value is not None:
            lines.append(f"{opt.key} = {ini_value(default_value)}")
        else:
            if mandatory:
                placeholder = example if example is not None else "<REQUIRED>"
                lines.append(f"# {opt.key} = {ini_value(placeholder)}  ; required")
            else:
                if example is not None:
                    lines.append(f"# {opt.key} = {ini_value(example)}  ; optional")
                else:
                    lines.append(f"# {opt.key} =  ; optional")
    lines.append("```\n")

    return "\n".join(lines)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for key, path in CONFIG_SOURCES.items():
        if not os.path.exists(path):
            print(f"[WARN] Skipping {key} — {path} not found")
            continue

        module = load_module_from_path(f"{key}_config", path)
        classes = find_config_classes(module)
        if not classes:
            print(f"[INFO] No config classes found in {key}")
            continue

        # Build snake_case filename from the CONFIG_SOURCES key
        def snake_case(s: str) -> str:
            s = s.strip().lower()
            s = re.sub(r"[^a-z0-9]+", "_", s)
            s = re.sub(r"_+", "_", s)
            return s.strip("_")

        out_path = os.path.join(DOCS_DIR, f"{snake_case(key)}_config.md")
        print(f"[+] Writing {out_path}")

        with open(out_path, "w", encoding="utf-8") as f:
            for cls in classes:
                f.write(generate_markdown_for_class(cls, heading_name=key))
                f.write("\n---\n")


if __name__ == "__main__":
    main()
