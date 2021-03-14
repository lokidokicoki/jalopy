import configparser
from shutil import copyfile
from os.path import exists
import argparse
import db
import cli
import app

DEBUG = False
args = None


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if args.no_backup is False:
        if exists(config["db"]["path"]):
            print("Shared DB exists")
            copyfile(config["db"]["path"], "jalopy.db")
        else:
            print("Shared DB not found, we will fix it!")
    else:
        print("Not using backup")

    db.init()
    db.createDB()

    # if cli
    if args.mode == "cli":
        cli.main()
    elif args.mode == "gui":
        app.main()
    else:
        print("Unknown mode, exiting")

    db.conn.close()

    if args.no_backup is False:
        copyfile("jalopy.db", config["db"]["path"])
    print("Night night")


parser = argparse.ArgumentParser(description="Jalo.py")
parser.add_argument("-m", "--mode", default="cli", help="use gui")
parser.add_argument("-d", "--debug", help="use debug", action="store_true")
parser.add_argument("-n", "--no-backup", help="do not use backup", action="store_true")
args = parser.parse_args()

DEBUG = args.debug

main()
