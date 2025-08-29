# -*- coding: utf-8 -*-
#  Copyright (c) 2020 - 2025 Ricardo Bartels. All rights reserved.
#  Copyright (c) 2025 Sol1. All rights reserved.
#
#  netbox-sync.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.

import os
import sys
from loguru import logger

DEFAULT_LOG_LEVELS = ['TRACE', 'DEBUG3', 'DEBUG2', 'DEBUG',
                      'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
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
    register_debug2_logging_level()

    # Check log level is valid
    if log_level not in available_log_levels:
        logger.error(
            f"Log level '{log_level}' is not an available log level, must be one of [{', '.join(available_log_levels)}].")

    # If the log level is DEBUG3 (old logger), change it to TRACE (new logger)
    elif log_level == 'DEBUG3':
        log_level = 'TRACE'

    # Because the library comes with a logger to std.err initalized and we get rid of that
    logger.remove()

    # if everything goes to the screen use the passed in log level otherwise use error
    _screen_log_level = "ERROR"
    if log_to_screen:
        _screen_log_level = log_level

    # Now add the screen std.err logger back using the right log level
    add_screen_log(_screen_log_level)

    # Add file logging if required
    if enable_log_file:
        if log_file is None or log_file == "":
            logger.critical("Log file name is empty, cannot log to file.")
        else:
            if os.path.isfile(log_file):
                if not os.access(log_file, os.W_OK):
                    print(
                        "Permissions error, unable to write to log file ({})".format(log_file)
                    )
                    sys.exit(os.EX_CONFIG)

            logger.add(log_file,
                       colorize=True,
                       format=get_log_formats(_screen_log_level, True),
                       level=log_level,
                       rotation=log_rotate,
                       retention=log_retention,
                       compression="gz"
                       )

    logger.debug(
        f"Log initalized with level: {log_level}, log to screen: {log_to_screen}, enable log file: {enable_log_file}, file: {log_file}, rotate: {log_rotate}, retention: {log_retention}")

def get_log_formats(log_level, process_id=False):
    """
    Return a log format template based on the provided log level and process_id flag.
    Parameters:
        log_level (str): Log level name (e.g., 'TRACE', 'DEBUG', 'INFO') which controls
                         whether class path, function and line number are included.
        process_id (bool): If True include the process id in the format.
    Returns:
        str: A formatted log string template containing timestamp, optional process id,
             optional debug context, log level and message.
    """
    _process_format = " <yellow>({process.id})</yellow> " if process_id else " "
    _debug_format = " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> " if log_level in ['TRACE', 'DEBUG2', 'DEBUG'] else " "

    return f"<blue>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</blue>{_process_format}{_debug_format}<level>{{level}}</level>: {{message}}"

def add_screen_log(log_level):
    """
    Add a screen (stderr) log handler to the application's logger.
    Parameters
    ----------
    log_level : int or str
        The log level to set for the screen handler (e.g. logging.INFO or "INFO").
    Returns
    -------
    None
    """

    logger.add(sys.stderr,
               colorize=True,
               level=log_level,
               backtrace=True,
               diagnose=True,
               format=get_log_formats(log_level)
               )


def debug2(self, message, *args, **kwargs):
    """Log a message at the custom "DEBUG2" level.

    Forwards all positional and keyword arguments to self.log.
    """

    return self.log("DEBUG2", message, *args, **kwargs)

def register_debug2_logging_level():
    """Register a custom "DEBUG2" level and attach a logger.debug2 helper."""
    # Define the custom level for DEBUG2 (below DEBUG=10, so we’ll give it 8)
    logger.level("DEBUG2", no=8, color="<cyan>", icon="🔍")
    # Add a helper method we can call as logger.debug2()
    logger.__class__.debug2 = debug2


