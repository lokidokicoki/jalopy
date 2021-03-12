import configparser
from shutil import copyfile
from os.path import exists
import db
import cli

selectedVehicle = None
config = configparser.ConfigParser()
config.read("config.ini")
print(config["db"]["path"])


def main():
    if exists(config["db"]["path"]):
        print("Shared DB exists")
        copyfile(config["db"]["path"], "jalopy.db")
    else:
        print("Shared DB not found, we will fix it!")
    db.createDB()

    # if cli
    cli.main()

    db.conn.close()
    copyfile("jalopy.db", config["db"]["path"])
    print("Night night")


main()
