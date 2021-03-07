import sqlite3
import datetime
import tkinter as tk

conn = sqlite3.connect("jalopy.db")
cursor = None

def createDB():
    cursor = conn.cursor()
    sql = "SELECT name from sqlite_master WHERE type='table' and name=?"

    # test for vehicles record
    cursor.execute(sql,["VEHICLES"])
    result = cursor.fetchone()

    if result is None:
        print("create jalopy.db tables")
        cursor.executescript("""
            CREATE TABLE VEHICLES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                REG_NO CHAR(10) NOT NULL,
                MAKE TEXT NOT NULL,
                MODEL TEXT NOT NULL,
                YEAR INTEGER NOT NULL,
                PURCHASE_DATE TEXT,
                PURCHASE_PRICE REAL,
                FUEL_TYPE_ID INTEGER NOT NULL,
                FUEL_CAPACITY REAL,
                OIL_TYPE TEXT,
                OIL_CAPACITY REAL,
                TYRE_SIZE_FRONT TEXT,
                TYRE_SIZE_REAR TEXT,
                TYRE_PRESSURE_FRONT REAL,
                TYRE_PRESSURE_REAR REAL
            );

            CREATE TABLE FUEL_TYPES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL
            );

            INSERT INTO FUEL_TYPES(NAME) VALUES('Unleaded');
            INSERT INTO FUEL_TYPES(NAME) VALUES('Super Unleaded');
            INSERT INTO FUEL_TYPES(NAME) VALUES('Diesel');
            INSERT INTO FUEL_TYPES(NAME) VALUES('Super Diesel');

            CREATE TABLE RECORDS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                VEHICLE_ID INTEGER NOT NULL,
                RECORD_TYPE_ID CHAR(1) NOT NULL,
                DATE TEXT NOT NULL,
                ODOMETER INTEGER NOT NULL,
                TRIP REAL,
                COST REAL NOT NULL,
                ITEM_COUNT REAL,
                NOTES TEXT
            );

            CREATE TABLE RECORD_TYPES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL
            );
            INSERT INTO RECORD_TYPES(NAME) VALUES('Fuel');
            INSERT INTO RECORD_TYPES(NAME) VALUES('Service');
            INSERT INTO RECORD_TYPES(NAME) VALUES('Maintenance');
            INSERT INTO RECORD_TYPES(NAME) VALUES('Tax');
            INSERT INTO RECORD_TYPES(NAME) VALUES('Insurance');
            INSERT INTO RECORD_TYPES(NAME) VALUES('M.O.T.');
            """)
        conn.commit();
    else:
        print("DB already exists")


createDB()
conn.close();


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self,text="Qit", fg="red",
                command=self.master.destroy)
        
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi yall")

root = tk.Tk()
app = Application(master = root)
app.mainloop()
