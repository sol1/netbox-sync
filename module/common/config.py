# -*- coding: utf-8 -*-
#  Copyright (c) 2020 - 2025 Ricardo Bartels. All rights reserved.
#
#  netbox-sync.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.


from module.config.option import ConfigOption
from module.config.base import ConfigBase
from module.config import common_config_section_name
from module.common.logging import LOG_FILE_MAX_ROTATION, LOG_FILE_MAX_SIZE_IN_MB


class CommonConfig(ConfigBase):
    """Controls the parameters for logging
    """

    section_name = common_config_section_name

    def __init__(self):
        self.options = [
            ConfigOption("log_level",
                         str,
                         description="""\
                         Logs will always be printed to stdout/stderr.
                         Logging can be set to following log levels:
                           ERROR:      Fatal Errors which stops regular a run
                           WARNING:    Warning messages won't stop the syncing process but mostly worth
                                       to have a look at.
                           INFO:       Information about objects that will be create/updated/deleted in NetBox
                           DEBUG:      Will log information about retrieved information, changes in internal
                                       data structure and parsed config
                           DEBUG2:     Will also log information about how/why data is parsed or skipped.
                           DEBUG3:     Logs all source and NetBox queries/results to stdout. Very useful for
                                       troubleshooting, but will log any sensitive data contained within a query.
                           TRACE:      Same as DEBUG3.
                         """,
                         default_value="INFO"),

            ConfigOption("log_to_file",
                         bool,
                         description="""Enabling this options will write all
                         logs to a log file defined in 'log_file'
                         """,
                         default_value=False),

            ConfigOption("log_file",
                         str,
                         description=f"""Destination of the log file if "log_to_file" is enabled.
                         Log file will be rotated maximum {LOG_FILE_MAX_ROTATION} times once
                         the log file reaches size of {LOG_FILE_MAX_SIZE_IN_MB} MB
                         """,
                         default_value="log/netbox_sync.log"),
            
            ConfigOption("log_lastrun_errors",
                         bool,
                         description="""Enabling this options will write all errors for this run only 
                         to a separate file called 'netbox-sync-lastrun-errors.log' in the same directory
                         as netbox-sync.py.
                         """,
                         default_value=False),
        ]

        super().__init__()
