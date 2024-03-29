"""
Main runner for the app.

Will spin up the cli or gui based on passed args.
"""

import argparse
import configparser
from os.path import exists, join
from shutil import copyfile

from jalopy.db.dbclient import DatabaseClient
from jalopy.entities.entity_manager import EntityManager
from jalopy.ui import Cli, Gui


def main(args_):
    """
    Bootstrap the program
    """
    config = configparser.ConfigParser()
    config.read(args_.options)
    cache_path = join(config["cache"]["path"], "jalopy.db")

    if args_.no_backup is False:
        if exists(config["db"]["path"]):
            print("Shared DB exists")
            copyfile(config["db"]["path"], cache_path)
        else:
            print("Shared DB not found, we will fix it!")
    else:
        print("Not using backup")

    dbclient = DatabaseClient(cache_path)
    # TODO: move to ctor
    dbclient.create_database()

    entity_manager = EntityManager(dbclient)

    entity_manager.load()

    # if cli
    user_interface = None
    if args_.mode == "cli":
        user_interface = Cli(entity_manager)
    elif args_.mode == "gui":
        user_interface = Gui(entity_manager)
    else:
        print("Unknown mode, fallback to cli")
        user_interface = Cli(entity_manager)

    user_interface.main()

    dbclient.conn.close()

    if args_.no_backup is False:
        copyfile(cache_path, config["db"]["path"])
    print("Night night")


parser = argparse.ArgumentParser(description="Jalo.py")
parser.add_argument("-o", "--options", required=True, help="path to config file")
parser.add_argument("-m", "--mode", default="cli", help="use gui")
parser.add_argument("-d", "--debug", help="use debug", action="store_true")
parser.add_argument("-n", "--no-backup", help="do not use backup", action="store_true")
args = parser.parse_args()

if __name__ == "__main__":
    main(args)
