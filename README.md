# timetracking

## What's this for?
This script will update the Team Python timetracking spreadsheet with the current time. On the first run of the day, the script updates the start time. After that, when start time has already been filled, each additional run keeps updating the end time.

## Requirements:
```bash
pip3 install --upgrade oauth2client gspread
```

## Usage:
```bash
python3 timetrack.py [--start | --end] <spreadsheet-id> <worksheet-name> <path-to-credentials-json>
```
With example arguments:
```bash
python3 timetrack.py --start 1HYUt1Y0UVAvGLRsBb6Esbsj6hnc3hI0XmHHHzbRlbnb James /home/james/credentials.json
```
Ask another team member for the credentials file. The spreadsheet id you'll find in the spreadsheet URL.


## Setup for easy usage
To make running the script easier, I recommend creating a shell script in your path (or an alias) that runs the script with the correct configuration for you. For instance, have a file called `~/bin/timetrack` with the following content (edit the arguments though):
```
#!/usr/bin/env bash

python3 /home/james/dev/timetracking/timetrack.py 1HYUt1Y0UVAvGLRsBb6Esbsj6hnc3hI0XmHHHzbRlbnb James /home/james/credentials.json
```

Make the script executable with
```bash
chmod +x ~/bin/timetrack
```

After this, you can simply run the script by running
```bash
timetrack
```


## Run automation
Make the following cronjob (edit the path to the shell script to what you set up for yourself earlier):
```
*/15 * * * * ~/bin/timetrack >/dev/null 2>&1
```
Also configure your machine to run `timetrack` once on startup so you don't lose the first 15 minutes.

