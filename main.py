"""Main runner for the app.

Will spin up the cli or gui based on passed args.
"""
from shutil import copyfile
from os.path import exists
import configparser
import argparse

from db import dbclient

import cli
import app


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

    dbclient.init()
    dbclient.createDatabase()

    # if cli
    if args_.mode == "cli":
        cli.main()
    elif args_.mode == "gui":
        app.main()
    else:
        print("Unknown mode, exiting")

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
