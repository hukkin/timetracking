from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time
import argparse


"""
Requirements:
pip3 install --upgrade oauth2client gspread

Usage example:
python3 timetrack.py (start | end) <spreadsheet-id> <worksheet-name> <path-to-credentials-json>
e.g.
python3 timetrack.py start 1HYUt1Y0UVAvGLRsBb6Esbsj6hnc3hI0XmHHHzbRlbnb James /home/james/credentials.json
"""

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
start_parser = subparsers.add_parser('start')
end_parser = subparsers.add_parser('end')

parser.add_argument('spreadsheet', help='Spreadsheet id')
parser.add_argument('worksheet', help='Worksheet name')
parser.add_argument('credentials', help='Credentials json path')

args = parser.parse_args()


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(args.credentials, scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key(args.spreadsheet)
worksheet = sheet.worksheet(args.worksheet)
date_cell = worksheet.find(time.strftime("%d.%m.%Y"))
column_offset = 1 if args.command == 'start' else 2
worksheet.update_cell(date_cell.row, date_cell.col + column_offset, time.strftime("%H:%M"))
