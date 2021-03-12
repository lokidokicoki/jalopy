import configparser
from shutil import copyfile
from os.path import exists
import argparse
import db
import cli


def main(mode):
    config = configparser.ConfigParser()
    config.read("config.ini")
    if exists(config["db"]["path"]):
        print("Shared DB exists")
        copyfile(config["db"]["path"], "jalopy.db")
    else:
        print("Shared DB not found, we will fix it!")
    db.createDB()

    # if cli
    if mode == "cli":
        cli.main()
    else:
        print("gui")

    db.conn.close()
    copyfile("jalopy.db", config["db"]["path"])
    print("Night night")


parser = argparse.ArgumentParser(description="Jalo.py")
parser.add_argument("-m", "--mode", default="cli", help="use gui")
args = parser.parse_args()

main(args.mode)
