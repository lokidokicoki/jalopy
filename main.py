"""Main runner for the app.

Will spin up the cli or gui based on passed args.
"""
from shutil import copyfile
from os.path import exists
import configparser
import argparse

from db.dbclient import DatabaseClient

from ui import Cli, Gui
import utils


def main(args_):
    """
    Bootstrap the program
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    if args_.no_backup is False:
        if exists(config["db"]["path"]):
            print("Shared DB exists")
            copyfile(config["db"]["path"], "jalopy.db")
        else:
            print("Shared DB not found, we will fix it!")
    else:
        print("Not using backup")

    dbclient = DatabaseClient("jalopy.db")
    dbclient.create_database()

    utils.set_dbclient(dbclient)

    # if cli
    user_interface = None
    if args_.mode == "cli":
        user_interface = Cli(dbclient)
    elif args_.mode == "gui":
        user_interface = Gui(dbclient)
    else:
        print("Unknown mode, exiting")
        exit()

    user_interface.main()

    dbclient.conn.close()

    if args_.no_backup is False:
        copyfile("jalopy.db", config["db"]["path"])
    print("Night night")


parser = argparse.ArgumentParser(description="Jalo.py")
parser.add_argument("-m", "--mode", default="cli", help="use gui")
parser.add_argument("-d", "--debug", help="use debug", action="store_true")
parser.add_argument("-n", "--no-backup", help="do not use backup", action="store_true")
args = parser.parse_args()


main(args)
