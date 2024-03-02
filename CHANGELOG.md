## v6.0.0 (2024-03-02)

### Refactor

- new line length, doc comments. LSP fixes

## v5.0.2 (2023-12-02)

### Fix

- **pyproject**: add version sync, update pakcages

## v5.0.1 (2023-05-31)

### Fix

- path to venv

## v5.0.0 (2023-05-31)

### Feat

- **Makefile**: new venv dir `/opt/venvs/PROJECT. better clean rule. better test output

### Fix

- update lock and requirements files
- **Makefile**: uninstall, not clean

### Refactor

- rename github repo, update project name

## v4.2.1 (2023-05-27)

### Fix

- update lock and requirements files
- **scripts**: set execute bits. update config path
- **bin**: use new cache dir for local copy of db
- **Makefile**: use config and cahe dirs under home directory

## v4.2.0 (2023-03-08)

### Feat

- **utils**: calculate total miles and cost per mile (#11)

### Fix

- update lock and requirements files
- linter fixes, standardise whitesspace to use tab character

## v4.1.1 (2023-03-01)

### Fix

- **system**: clean up shell paths

## v4.1.0 (2022-06-12)

### Fix

- **pyproject**: correct version number
- **cli**: use f-strings for display. default to `fuel` for record entry
- **cli**: import order
- **plots**: force use of tkinter

### Feat

- inlcude commitizen settings
- **entity_manager**: on save call `dbclient.commit`
- **dbclient**: add `commit` method
- **scripts**: new driver script to run app

## v4 (2021-08-30)

### Feat

- linter fixes
- render mpg chart #1
- import plots module and hook up to menu #1
- plot the historic fuel price  #1
- new `get_records_by_type` (#1)
- **cli**: stub plot menu, convert spaces to tabs #1
- set uid of entities post save
- on `create`, return newly created row

## v3 (2021-08-26)

### Feat

- cli new record `list` mode. revised record summary
- ui/cli: implement validation

## 3.0 (2021-07-31)

### Fix

- restructure code, rename main file (#4)

## 2.0 (2021-07-31)

### Feat

- nicer record summary
- split out EntityType class. better record summary. sort by date.
- new liner config file
- ui: implement removal
- implement removal
- cli: isoformat dates, use new save mechanisms
- use isoformat dates. only load unarchived rows. convert date instances to strings. use new db baseitem crud ops
- entities: include new archived field
- utils: fix up uid
- base_item defines CRUD operations. include `archived` column on vehicle and record tables
- cli: revised for inquirer package. new helper functions for default fetching. TODO: handle saving
- rename `netity_id` as `uid` to match db. linter fixes
- db: rename `id` to `uid` to prevent class with python `id` method
- ui: rework for new entity classes
- db: clean up module names
- entities: update manager
- entities: add init.py
- db: rework db table and column names
- update ui and entities to read from correct places
- main: refactor to instatiate entity manager
- utils: convert to class, update for new entity manager methods
- ui: refactor ui to use new entity_manager
- entities: update manager to load and cache entities
- db: new base_item
- entities: new fuel_type and record_type
- db: convert vehicles and records to classes. update dbcluent to suit
- main: update for new ui classes
- ui: convert gui and cli to classes. inherit from base_ui
- db: convert to a class, rename functions and variables to comply with pylint
- utils: clean up variable names
- add base_ui class and init file
- clean up makefile
- move gui and cli to `ui` module
- new entities; base class, record and vehicle derived classes and entity manager. TODO: implement usage
- inlcude Makefile with lint rule, runs isort, flake8 and pylint
- include .pylintrc

### Fix

- ui: correct order of checks

## v1.0 (2021-07-19)

## 0.1 (2021-03-29)

### Feat

- **gitignore**: exclude config.ini
- **config**: remove file, this can change per machine
- **main**: cache parsed args. check for `no backup`
- **db**: new init function
- **main**: handle debug and mode options
- **app**: new `main` function
- **cli**: include PURCHASE_ODOMETER field
- **db**: include PRUCHASE_ODOMETER on VEHICLE table
- **utils**: only calculate fuel if there are fuel records
- **app**: s/MyWin/MainWindow
- **setup.py**: a setup file
- **main**: add in argparse to control either gui or cli mode
- **cli**: refactoring; createEditXXX=>XXXForm, conflate getFuelTyps & getRecordTypes as getTypeChoices
- **main**: refactor for new cli and utils modules
- **cli**: split out cli into own module
- **utils**: split out utility functions
- **setup**: include flake overrides
- **main**: refactor for updated db functions. refactorfor corrected RECORD_TYPE_ID. Reorder stats output
- **db**: RECORDS.RECORD_TYPE_ID is now an INTEGER. rename `load` functions as `get`
- **app**: stub gtk
- **requirements**: python deps
- **main**: linter fixes
- **db**: linter fixes
- **main**: display stats for selected vehicle, incl. mpg, record counts
- **main**: implement editing of records
- **db**: refactor s/loadRecord/loadRecords
- **db**: clean up insert and update
