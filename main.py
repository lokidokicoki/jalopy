import sqlite3
import datetime
from collections import defaultdict
from PyInquirer import prompt, Separator
import configparser
from shutil import copyfile
from os.path import exists
import pprint
import db

pp = pprint.PrettyPrinter(indent=2)
selectedVehicle = None
running = True
config = configparser.ConfigParser()
config.read('config.ini')
print(config['db']['path'])

litresPerGallon = 4.54609
kmPerMile = 1.60934
mpgToL100km = 235.215

def getFuelTypes(answers):
    """
    Get fuel types
    """
    types = db.getFuelTypes()
    choices = [{'name':i[1],'value':i[0]} for i in types]

    return choices 

def getRecordTypes(answers):
    """
    Get record types
    """
    types = db.getRecordTypes()
    choices = [{'name':i[1],'value':i[0]} for i in types]

    return choices 

def calculateEconomy(record, silent=False):
    """
    mpg
    l/100km
    km/l
    """
    tripKm = record['TRIP'] * kmPerMile

    kpl = tripKm/record['ITEM_COUNT']
    mpg = record['TRIP']/(record['ITEM_COUNT']/litresPerGallon)
    l100 = mpgToL100km / mpg

    if silent is False:
        print('{:0.2f} mpg'.format(mpg))
        print('{:0.2f} kpl'.format(kpl))
        print('{:0.2f} l/100Km'.format(l100))

    return {'mpg':mpg, 'kpl':kpl, 'l100':l100}

def createEditVehicle(vehicle=None):
    """
    Create/edit vehicle
    """
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

def createEditRecord(record=None):
    """
    Create/edit 'record'
    """
    allVehicles = db.loadVehicles()
    questions = [
        {
            'type':'list',
            'name':'VEHICLE_ID',
            'message':'Reg. No.:',
            'default': record['VEHICLE_ID'] if record else '',
            'choices':[{'name':i[1],'value':i[0]} for i in allVehicles]
        },
        {
            'type':'list',
            'name':'RECORD_TYPE_ID',
            'message':'Type',
            'default': record['RECORD_TYPE_ID'] if record else '',
            'choices':getRecordTypes
        },
        {
            'type':'input',
            'name':'DATE',
            'message':'Date',
            'default': record['DATE'] if record else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'ODOMETER',
            'message':'Odometer',
            'default': str(record['ODOMETER']) if record else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'TRIP',
            'message':'Trip (optional)',
            'default': str(record['TRIP']) if record else '',
        },
        {
            'type':'input',
            'name':'COST',
            'message':'Cost',
            'default': str(record['COST']) if record else '',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'ITEM_COUNT',
            'message':'Item Count',
            'default': str(record['ITEM_COUNT']) if record else '1',
            'validate': lambda val: len(val) != 0 or 'Please supply a value'
        },
        {
            'type':'input',
            'name':'NOTES',
            'message':'Notes (optional)',
            'default': record['NOTES'] if record else '',
        },
    ]

    answers = prompt(questions)


    # process, then saveo
    if(record):
        answers['ID'] = record['ID']

    answers['VEHICLE_ID'] = int(answers['VEHICLE_ID'])
    answers['RECORD_TYPE_ID'] = int(answers['RECORD_TYPE_ID'])
    answers['ODOMETER'] = int(answers['ODOMETER'])
    answers['TRIP'] = float(answers['TRIP'])
    answers['COST'] = float(answers['COST'])
    answers['ITEM_COUNT'] = float(answers['ITEM_COUNT'])

    # if it is a fuel record, calculate & display the fuel economy
    if answers['RECORD_TYPE_ID'] == 1:
        calculateEconomy(answers)

    db.addRecord(answers)

def selectVehicle():
    """
    Prompt user to select a vehicle
    """
    allVehicles = db.loadVehicles()

    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Select vehicle',
            'choices':[{'name':i[1],'value':i[0]} for i in allVehicles]
        }
    ]

    answers = prompt(questions)

    return next(x for x in allVehicles if x[0] == answers['opts'])

def selectRecord(vehicle):
    """
    Select a record for a specific vehicle
    """
    allRecords = db.loadRecords(vehicle['ID'])

    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Select record',
            'choices':[{'name':i['DATE'],'value':i['ID']} for i in allRecords]
        }
    ]

    answers = prompt(questions)

    return next(x for x in allRecords if x[0] == answers['opts'])

def stats(vehicle):
    """
    Accumulative stats for this vehicle
    """

    # get all records for this vehicle
    records = db.loadRecords(vehicle['ID'])
    types = db.getRecordTypes()
    totalCost = 0
    avgMpg = 0
    avgKpl = 0
    avgL100 = 0
    counts = [ {'id':x['ID'],'name':x['NAME'], 'count':0} for x in types ]

    for record in records:
        count = next(x for x in counts if x['id'] == int(record['RECORD_TYPE_ID']))
        count['count'] = count['count'] + 1
        if record['RECORD_TYPE_ID'] == '1':
            eff = calculateEconomy(record, True)

            avgMpg= avgMpg + eff['mpg']
            avgKpl= avgKpl + eff['kpl']
            avgL100= avgL100 + eff['l100']

        totalCost = totalCost + record['COST']
    fuelCount = next(x for x in counts if x['id'] == 1)

    print('Avg. MPG: {:0.2f}'.format(avgMpg/fuelCount['count']))
    print('Avg. km/l: {:0.2f}'.format(avgKpl/fuelCount['count']))
    print('Avg. l/100Km: {:0.2f}'.format(avgL100/fuelCount['count']))
    print('Total cost: {:0.2f}'.format(totalCost))

    print('Record counts:')
    for i in counts:
        print('{}: {}'.format(i['name'], i['count']))

def recordsMenu():
    """
    CRUD ops for records
    """
    questions = [
        {
            'type':'list',
            'name':'opts',
            'message':'Records menu',
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
        print('add record')
        createEditRecord()
    elif answers['opts'] == 'edit':
        print('edit vehicle')
        vehicle = selectVehicle()
        record = selectRecord(vehicle)
        print(record)
        createEditRecord(record)
    elif answers['opts'] == 'remove':
        print('remove vehicle')
    else:
        print('return to main')
    
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
                {
                    'name':'Stats',
                    'value':'stats'
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
    elif answers['opts'] == 'stats':
        print('stats vehicle')
        vehicle = selectVehicle()
        stats(vehicle)
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
        print('mod vehicles')
        vehiclesMenu()
    elif answers["opts"] == 'records':
        print('mod records')
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
