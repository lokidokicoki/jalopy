import sqlite3
import datetime
from collections import defaultdict
from PyInquirer import prompt, Separator
import configparser
from shutil import copyfile
from os.path import exists
import db

selectedVehicle = None
running = True
config = configparser.ConfigParser()
config.read('config.ini')
print(config['db']['path'])



def getFuelTypes(answers):
    types = db.getFuelTypes()
    choices = [{'name':i[1],'value':i[0]} for i in types]

    return choices 

def createEditVehicle(vehicle=None):
    questions = [
        {
            'type':'input',
            'name':'REG_NO',
            'message':'Reg. No.:',
            'default': vehicle['REG_NO'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'MAKE',
            'message':'Make',
            'default': vehicle['MAKE'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'MODEL',
            'message':'Model',
            'default': vehicle['MODEL'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'YEAR',
            'message':'Year',
            'default': str(vehicle['YEAR']) if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'PURCHASE_DATE',
            'message':'Purchase Date',
            'default': vehicle['PURCHASE_DATE'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'PURCHASE_PRICE',
            'message':'Purchase Price',
            'default': str(vehicle['PURCHASE_PRICE']) if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'list',
            'name':'FUEL_TYPE_ID',
            'message':'Fuel type',
            'choices':getFuelTypes,
            'default': vehicle['FUEL_TYPE_ID'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'FUEL_CAPACITY',
            'message':'Fuel Capacity (ltr)',
            'default': str(vehicle['FUEL_CAPACITY']) if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'OIL_TYPE',
            'message':'Oil Type',
            'default': vehicle['OIL_TYPE'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'OIL_CAPACITY',
            'message':'Oil Capacity (ltr)',
            'default': str(vehicle['OIL_CAPACITY']) if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'TYRE_SIZE_FRONT',
            'message':'Tyre size front',
            'default': vehicle['TYRE_SIZE_FRONT'] if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'TYRE_PRESSURE_FRONT',
            'message':'Tyre pressure front',
            'default': str(vehicle['TYRE_PRESSURE_FRONT']) if vehicle else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'TYRE_SIZE_REAR',
            'message':'Tyre size rear',
            'default': lambda answers: vehicle['TYRE_SIZE_REAR'] if vehicle else answers['TYRE_SIZE_FRONT'],
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'TYRE_PRESSURE_REAR',
            'message':'Tyre pressure rear',
            'default': lambda answers: str(vehicle['TYRE_PRESSURE_REAR']) if vehicle else answers['TYRE_PRESSURE_FRONT'],
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
    ]

    answers = prompt(questions)


    # process, then save
    answers['REG_NO'] = answers['REG_NO'].upper()
    answers['MAKE'] = answers['MAKE'].lower().capitalize()
    answers['MODEL'] = answers['MODEL'].lower().capitalize()
    answers['YEAR'] = int(answers['YEAR'])
    answers['PURCHASE_PRICE'] = float(answers['PURCHASE_PRICE'])
    answers['FUEL_CAPACITY'] = float(answers['FUEL_CAPACITY'])
    answers['OIL_CAPACITY'] = float(answers['OIL_CAPACITY'])
    answers['FUEL_TYPE_ID`'] = int(answers['FUEL_TYPE_ID'])
    answers['TYRE_PRESSURE_FRONT`'] = float(answers['TYRE_PRESSURE_FRONT'])
    answers['TYRE_PRESSURE_REAR`'] = float(answers['TYRE_PRESSURE_REAR'])

    if(vehicle):
        answers['ID'] = vehicle['ID']

    db.addVehicle(answers)

def selectVehicle():
    allVehicles = db.loadVehicles()
    print(allVehicles)

    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Select vehicle to edit',
            'choices':[{'name':i[1],'value':i[0]} for i in allVehicles]
        }
    ]

    answers = prompt(questions)

    print(answers)
   
    return next(x for x in allVehicles if x[0] == answers['opts'])

def vehiclesMenu():
    """
    CRUD ops for vehicles
    """
    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Vehicle menu',
            'choices':[
                {
                    'name':'Add',
                    'value':'add'
                },
                {
                    'name':'Edit',
                    'value':'edit'
                },
                {
                    'name':'Remove',
                    'value':'remove'
                },
                Separator(),
                {
                    'name':'Back',
                    'value':'back'
                },
            ]
        }
    ]

    answers = prompt(questions)

    if answers['opts'] == 'add':
        print('add vehicle')
        createEditVehicle()
    elif answers['opts'] == 'edit':
        print('edit vehicle')
        vehicle = selectVehicle()
        createEditVehicle(vehicle)
    elif answers['opts'] == 'remove':
        print('remove vehicle')
    else:
        print('return to main')
    

def mainMenu():
    """
    Main menu
    """
    global running

    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Things to do',
            'choices':[
                {
                    'name':'Vehicles',
                    'key':'v',
                    'value':'vehicles'
                },
                {
                    'name':'Records',
                    'key':'r',
                    'value':'records'
                },
                Separator(),
                {
                    'name': 'Exit',
                    'key':'x',
                    'value':'exit'
                }
            ]
        }
    ]   

    answers = prompt(questions)


    if answers['opts'] == 'exit':
        running = False
    elif answers["opts"] == 'vehicles':
        print('load vehicle')
        vehiclesMenu()
    elif answers["opts"] == 'records':
        print('add vehicle')
        recordsMenu()

def main():
    if exists(config['db']['path']):
        print('Shared DB exists')
        copyfile(config['db']['path'], 'jalopy.db')
    else:
        print('Shared DB not found, we will fix it!')
    db.createDB()

    while running:
        mainMenu()

    db.conn.close()
    copyfile('jalopy.db', config['db']['path'])
    print('Night night')

main()
