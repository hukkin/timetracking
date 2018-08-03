from oauth2client.service_account import ServiceAccountCredentials
import gspread
import argparse
import datetime


"""
Requirements:
pip3 install --upgrade oauth2client gspread

Usage:
python3 timetrack.py [--start | --end] <spreadsheet-id> <worksheet-name> <path-to-credentials-json>
e.g.
python3 timetrack.py --start 1HYUt1Y0UVAvGLRsBb6Esbsj6hnc3hI0XmHHHzbRlbnb James /home/james/credentials.json
"""
def round_minutes(dt, direction, resolution):
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    return dt + datetime.timedelta(minutes=new_minute - dt.minute)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--start', action='store_true')
group.add_argument('--end', action='store_true')
parser.add_argument('spreadsheet', help='Spreadsheet id')
parser.add_argument('worksheet', help='Worksheet name')
parser.add_argument('credentials', help='Credentials json path')
args = parser.parse_args()

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(args.credentials, scope)
gc = gspread.authorize(credentials)

now = datetime.datetime.now()

sheet = gc.open_by_key(args.spreadsheet)
worksheet = sheet.worksheet(args.worksheet)
date_cell = worksheet.find(now.strftime("%d.%m.%Y"))

cell_to_edit = (date_cell.row, date_cell.col + 1 + args.end)
if not args.start and not args.end:
    cell_to_edit = (cell_to_edit[0], cell_to_edit[1] + bool(worksheet.cell(*cell_to_edit).value))

rounding_direction = 'down' if cell_to_edit == start_cell else 'up'
rounded_now = round_minutes(now, rounding_direction, 15)

worksheet.update_cell(*cell_to_edit, rounded_now.strftime("%H:%M"))
