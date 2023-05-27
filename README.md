## What is it?

Simple fuel economy and maintenance cost tracking tool for multiple vehicles.

## Installation

This project uses poetry, so make sure that is installed.

Then run the following:

    poetry install

## Example config

On chromeos install <https://linuxhint.com/google_drive_installation_ubuntu/> ocamlfuse

```yaml
[db]
path=/mnt/chromeos/GoogleDrive/MyDrive/jalopy.db

[cache]
path=/home/<user>/.cache/jalo.py
```

Run it like this: `source scripts/run_jalopy.sh`
