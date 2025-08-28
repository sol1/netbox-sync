# -*- coding: utf-8 -*-
#  Copyright (c) 2020 - 2025 Ricardo Bartels. All rights reserved.
#
#  netbox-sync.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.

import os
import sys
from loguru import logger

from module.common.misc import do_error_exit

# # define DEBUG2 and DEBUG3 log levels
# DEBUG2 = 6  # extended messages
# DEBUG3 = 3  # extra extended messages

# # define valid log levels
# valid_log_levels = ["DEBUG3", "DEBUG2", "DEBUG", "INFO", "WARNING", "ERROR"]

# # add log level DEBUG2
# logging.addLevelName(DEBUG2, "DEBUG2")
# # add log level DEBUG3
# logging.addLevelName(DEBUG3, "DEBUG3")

# def debug2(self, message, *args, **kws):
#     if self.isEnabledFor(DEBUG2):
#         # Yes, logger takes its '*args' as 'args'.
#         self._log(DEBUG2, message, args, **kws)


# def debug3(self, message, *args, **kws):
#     if self.isEnabledFor(DEBUG3):
#         # Yes, logger takes its '*args' as 'args'.
#         self._log(DEBUG3, message, args, **kws)


# logging.Logger.debug2 = debug2
# logging.Logger.debug3 = debug3


# def get_logger():
#     """
#     common function to retrieve common log handler in project files

#     Returns
#     -------
#     log handler
#     """

#     return logging.getLogger("NetBox-Sync")

DEFAULT_LOG_LEVELS = ['TRACE', 'DEBUG3', 'DEBUG2', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
LOG_FILE_MAX_SIZE_IN_MB = 10
LOG_FILE_MAX_ROTATION = 5


def setup_logging(log_to_screen=False,
                enable_log_file=True,
                log_file=f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/netbox-sync.log",
                log_rotate=f'{LOG_FILE_MAX_SIZE_IN_MB} MB',
                log_retention=LOG_FILE_MAX_ROTATION,
                log_level='INFO',
                available_log_levels=DEFAULT_LOG_LEVELS,
                ):
    """
    Initalize logging.
    It defaults to logging to standard error for ERROR's and above plus a log_file, the log_file logs at the log_level.
    If log_to_screen is enabled, it will change the screen logging to the specified log_level.
    The log format includes the date and process id so you can identify all log entries from the same run.

    Args:
        log_to_screen (bool, optional): If True, change the screen logging to the log_level. Defaults to False.
        enable_log_file (bool, optional): If True, enables file logging. Defaults to True.
        log_file (str, optional): The path to the log file. Defaults to 'netbox-sync.log'.
        log_rotate (str, optional): The log file rotation policy. Defaults to '1 week'.
        log_retention (str, optional): The log file retention policy. Defaults to '3 weeks'.
        log_level (str, optional): The logging level. Defaults to 'WARNING'.
        available_log_levels (list, optional): A list of available logging levels. Aliased as available_log_levels. Defaults to DEFAULT_LOG_LEVELS.

    """
    def get_log_formats(log_level, process_id = False):
        """
        Returns screen and file log formats based on log level.
        """
        _process_format = " <yellow>({process.id})</yellow> " if process_id else " "
        _debug_format = " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> " if log_level in ['TRACE', 'DEBUG'] else " "

        return f"<blue>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</blue>{_process_format}{_debug_format}<level>{{level}}</level>: {{message}}"

    if log_level not in available_log_levels:
        logger.error(f"Log level '{log_level}' is not an available log level, must be one of [{', '.join(available_log_levels)}].")

    if log_level == 'DEBUG2':
        log_level = 'DEBUG'
    elif log_level == 'DEBUG3':
        log_level = 'TRACE'
    # Because the library comes with a logger to std.err initalized and we get rid of that
    logger.remove()

    # if everything goes to the screen use the passed in log level otherwise use error
    _screen_log_level = "ERROR" 
    if log_to_screen:
        _screen_log_level = log_level
    
    # Now add the screen std.err logger back using the right log level
    logger.add(sys.stderr, colorize=True,
                level=_screen_log_level,
                backtrace=True,
                diagnose=True,
                format=get_log_formats(_screen_log_level)
                )

    # Add file logging if required
    if enable_log_file:
        if log_file is None or log_file == "":
            logger.critical("Log file name is empty, cannot log to file.")
        else:
            if os.path.isfile(log_file):
                if not os.access(log_file, os.W_OK):
                    print("Permissions error, unable to write to log file ({})".format(log_file))
                    sys.exit(os.EX_CONFIG)

            logger.add(log_file, colorize=True,
                    format=get_log_formats(_screen_log_level, True),
                    level=log_level,
                    rotation=log_rotate,
                    retention=log_retention,
                    compression="gz"
                    )
    
    logger.debug(
        f"Log initalized with level: {log_level}, log to screen: {log_to_screen}, enable log file: {enable_log_file}, file: {log_file}, rotate: {log_rotate}, retention: {log_retention}")


# def setup_logging(log_level=None, log_file=None):
#     """
#     Set up logging for the whole program and return a log handler

#     Parameters
#     ----------
#     log_level: str
#         valid log level to set logging to
#     log_file: str
#         name of the log file to log to

#     Returns
#     -------
#     log handler to use for logging
#     """

#     if log_level is None or log_level == "":
#         do_error_exit("log level undefined or empty. Check config please.")

#     # check set log level against self defined log level array
#     if not log_level.upper() in valid_log_levels:
#         do_error_exit(f"Passed invalid log level: {log_level}")

#     # Set default log format
#     log_format = '%(asctime)s - %(levelname)s: %(message)s'

#     if log_level.startswith("DEBUG"):
#         log_format = '%(asctime)s - %(levelname)s: [%(filename)s:%(lineno)d]: %(message)s'

#     # Determine numeric log level and format
#     if log_level == "DEBUG2":
#         numeric_log_level = DEBUG2
#     elif log_level == "DEBUG3":
#         numeric_log_level = DEBUG3
#         logging.basicConfig(level=logging.DEBUG, format=log_format)
#     else:
#         numeric_log_level = getattr(logging, log_level.upper(), None)

#     log_format = logging.Formatter(log_format)

#     # create logger instance
#     logger = get_logger()

#     logger.setLevel(numeric_log_level)

#     # setup stream handler
#     # in DEBUG3 the root logger gets redefined, that would print every log message twice
#     if log_level != "DEBUG3":
#         log_stream = logging.StreamHandler(sys.stdout)
#         log_stream.setFormatter(log_format)
#         logger.addHandler(log_stream)

#     # setup log file handler
#     if log_file is not None:
#         # base directory is three levels up
#         base_dir = os.sep.join(__file__.split(os.sep)[0:-3])
#         if log_file[0] != os.sep:
#             log_file = f"{base_dir}{os.sep}{log_file}"

#         log_file_handler = None
#         try:
#             log_file_handler = RotatingFileHandler(
#                 filename=log_file,
#                 maxBytes=log_file_max_size_in_mb * 1024 * 1024,  # Bytes to Megabytes
#                 backupCount=log_file_max_rotation
#             )
#         except Exception as e:
#             do_error_exit(f"Problems setting up log file: {e}")

#         log_file_handler.setFormatter(log_format)
#         logger.addHandler(log_file_handler)

#     return logger
