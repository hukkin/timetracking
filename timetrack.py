#!/usr/bin/env python3

import argparse
import datetime
import os
import getpass
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

"""
Requirements:
pip3 install --upgrade oauth2client gspread

Usage example:
python3 timetrack.py (start | end | ) -s <spreadsheet-id> -w <worksheet-name> -c <path-to-credentials-json>
e.g.
python3 timetrack.py start 1HYUt1Y0UVAvGLRsBb6Esbsj6hnc3hI0XmHHHzbRlbnb James /home/james/credentials.json

Or, create .config.json in this directory storing the spreadsheet id and credential file path, then
try just running ./timetrack.py

If your username differs a lot from spreadsheet name, update fix_names

"""

def get_user():
    fix_names = {'hukkinj1': 'Taneli'}
    username = getpass.getuser()
    return fix_names.get(username, username.title())

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
start_parser = subparsers.add_parser('start')
end_parser = subparsers.add_parser('end')

try:
    with open('.config.json') as f:
        json_data = json.load(f)
    credentials = os.path.expanduser(json_data['credentials'])
    cred_names = ['-c', '--credentials']
except:
    credentials = None
    print('Warning: no .config.json, so you gotta pass stuff in.')

try:
    spread_id = json_data['spreadsheet']
    spread_names = ['-s', '--spreadsheet']
except:
    spread_id = None
    spread_names = ['spreadsheet']
    cred_names = ['credentials']

parser.add_argument(*spread_names, help='Spreadsheet id', default=spread_id)
parser.add_argument(*cred_names, help='Credentials json path', default=credentials)
parser.add_argument('-w', '--worksheet', help='Worksheet name', default=get_user())

args = parser.parse_args()

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(args.credentials, scope)
gc = gspread.authorize(credentials)

now = datetime.datetime.now()
sheet = gc.open_by_key(args.spreadsheet)
worksheet = sheet.worksheet(args.worksheet)
date_cell = worksheet.find(now.strftime("%d.%m.%Y"))

if not args.command:
    start_filled = worksheet.cell(date_cell.row, date_cell.col+1).value
    column_offset = 2 if start_filled else 1
elif args.command == 'start':
    column_offset = 1
else:
    column_offset = 2

worksheet.update_cell(date_cell.row, date_cell.col + column_offset, now.strftime('%H:%M'))
worked = None

# if we are doing end of day, do time worked as well
if column_offset == 2:
    column_offset = 4
    started = worksheet.cell(date_cell.row, date_cell.col+1).value
    delta = now - datetime.datetime.strptime(started, '%H:%M') - datetime.timedelta(minutes=30)
    worked = str(delta).rsplit(':', 1)[0].split(', ', 1)[-1]
    worksheet.update_cell(date_cell.row, date_cell.col + column_offset, worked)

worked = ' Worked: {} today.'.format(worked) if worked else ''
display = 'BEGIN' if column_offset == 1 else 'END'
printable = [display, args.worksheet, now.strftime('%H:%M'), now.strftime("%d.%m.%Y"), worked]

print('==========================================================')
print('Updated {} time log for {} at {} on date {}.{}'.format(*printable))
print('==========================================================')
