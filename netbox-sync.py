#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 - 2025 Ricardo Bartels. All rights reserved.
#
#  netbox-sync.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.

self_description = """
Sync objects from various sources to NetBox
"""


from datetime import datetime

from module.common.misc import grab, get_relative_time
from module.common.cli_parser import parse_command_line
from module.common.logging import setup_logging, add_screen_log
from module.netbox.connection import NetBoxHandler
from module.netbox.inventory import NetBoxInventory
from module.sources import instantiate_sources
from module.config.parser import ConfigParser
from module.common.config import CommonConfig
from module.config.file_output import ConfigFileOutput
from module import __version__, __version_date__, __description__

from loguru import logger

def main():

    # Add screen logging for startup so we can see what is happening before standard logging is set up
    logger.remove()
    add_screen_log(log_level="DEBUG")
    start_time = datetime.now()

    # parse command line
    args = parse_command_line(self_description=self_description)

    # write out default config file and exit if "generate_config" is defined
    ConfigFileOutput(args)

    # parse config files and environment variables
    config_parse_handler = ConfigParser()
    config_parse_handler.add_config_file_list(args.config_files)
    config_parse_handler.read_config()

    # read common config
    common_config = CommonConfig().parse(do_log=False)

    # cli option overwrites config file
    log_level = grab(args, "log_level", fallback=common_config.log_level)

    # remove startup screen logger and replace with standard logging
    logger.remove()
    # setup logging
    setup_logging(
        log_level=log_level, 
        enable_log_file=common_config.log_to_file, 
        log_file=common_config.log_file, 
        log_to_screen=args.log_to_screen, 
        log_lastrun_errors=common_config.log_lastrun_errors
        )

    # now we are ready to go
    logger.info(f"Starting {__description__} v{__version__} ({__version_date__})")
    for config_file in config_parse_handler.file_list:
        logger.info(f"Using config file: {config_file}")

    # exit if any parser errors occurred here
    config_parse_handler.log_end_exit_on_errors()

    # just to print config options to log/console
    CommonConfig().parse()

    # initialize an empty inventory which will be used to hold and reference all objects
    inventory = NetBoxInventory()

    # establish NetBox connection
    nb_handler = NetBoxHandler()

    # if purge was selected we go ahead and remove all items which were managed by this tools
    if args.purge is True:

        if args.dry_run is True:
            logger.error("Purge not available with option 'dry_run'")
            exit(1)

        nb_handler.just_delete_all_the_things()

        # that's it, we are done here
        exit(0)

    # instantiate source handlers and get attributes
    logger.info("Initializing sources")
    sources = instantiate_sources()

    # all sources are unavailable
    if len(sources) == 0:
        logger.error("No working sources found. Exit.")
        exit(1)

    # collect all dependent object classes
    logger.info("Querying necessary objects from NetBox. This might take a while.")
    for source in sources:
        nb_handler.query_current_data(source.dependent_netbox_objects)

    logger.info("Finished querying necessary objects from NetBox")

    # resolve object relations within the initial inventory
    inventory.resolve_relations()

    # initialize basic data needed for syncing
    nb_handler.initialize_basic_data()

    # loop over sources and patch netbox data
    for source in sources:
        logger.debug(f"Retrieving data from source '{source.name}'")
        source.apply()

    # add/remove tags to/from all inventory items
    inventory.tag_all_the_things(nb_handler)

    # update all IP addresses
    inventory.query_ptr_records_for_all_ips()

    if args.dry_run is True:
        logger.info("This is a dry run and we stop here. Running time: %s" %
                 get_relative_time(datetime.now() - start_time))
        exit(0)

    # update data in NetBox
    nb_handler.update_instance()

    # prune orphaned objects from NetBox
    nb_handler.prune_data()

    # delete tags which are not used anymore
    nb_handler.delete_unused_tags()

    # loop over sources and patch netbox data
    for source in sources:
        # closing all open connections
        source.finish()

    # closing NetBox connection
    nb_handler.finish()

    # finish
    logger.info("Completed NetBox Sync in %s" % get_relative_time(datetime.now() - start_time))


if __name__ == "__main__":
    main()

# EOF
