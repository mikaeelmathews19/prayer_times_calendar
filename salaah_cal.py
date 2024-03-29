import os
import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Path to the service account JSON key file
SERVICE_ACCOUNT_KEY_PATH = ''

# ID of the Google Sheet containing the salaah times
SHEET_ID = ''

# ID of the Google Calendar where you want to create the events
CALENDAR_ID = ''

# Authenticate and authorize the Google API client using service account credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH, scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/spreadsheets.readonly'])

# Build the Google Sheets and Google Calendar service
sheets_service = build('sheets', 'v4', credentials=credentials)
calendar_service = build('calendar', 'v3', credentials=credentials)

try:
    # Read data from the Google Sheet
    sheet_range = 'Sheet1!A2:F'  # Assuming the data starts from the second row
    sheet_result = sheets_service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=sheet_range).execute()
    sheet_data = sheet_result.get('values', [])

    print(f"Number of rows in sheet: {len(sheet_data)}")

    # Process each row in the sheet and create events in the Google Calendar
    for row in sheet_data:
        if len(row) < 6:
            continue
        
        date_str, fajr_time, thuhr_time, asr_time, maghreb_time, isha_time = row

        # Convert date and times to datetime objects
        date_obj = datetime.datetime.strptime(date_str, '%d/%m/%y').date()
        fajr_datetime = datetime.datetime.combine(date_obj, datetime.datetime.strptime(fajr_time, '%H:%M').time())
        thuhr_datetime = datetime.datetime.combine(date_obj, datetime.datetime.strptime(thuhr_time, '%H:%M').time())
        asr_datetime = datetime.datetime.combine(date_obj, datetime.datetime.strptime(asr_time, '%H:%M').time())
        maghreb_datetime = datetime.datetime.combine(date_obj, datetime.datetime.strptime(maghreb_time, '%H:%M').time())
        isha_datetime = datetime.datetime.combine(date_obj, datetime.datetime.strptime(isha_time, '%H:%M').time())

        # Create Fajr event
        fajr_event = {
            'summary': 'Fajr Salaah',
            'start': {
                'dateTime': fajr_datetime.isoformat(),
                'timeZone': 'Africa/Johannesburg',  # Replace with your timezone
            },
            'end': {
                'dateTime': (fajr_datetime + datetime.timedelta(minutes=15)).isoformat(),  # Assuming events last for 30 minutes
                'timeZone': 'Africa/Johannesburg',
            },
        }
        calendar_service.events().insert(calendarId=CALENDAR_ID, body=fajr_event).execute()

        # Create Thuhr event
        thuhr_event = {
            'summary': 'Thuhr Salaah',
            'start': {
                'dateTime': thuhr_datetime.isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': (thuhr_datetime + datetime.timedelta(minutes=15)).isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
        }
        calendar_service.events().insert(calendarId=CALENDAR_ID, body=thuhr_event).execute()

        # Create Asr event
        asr_event = {
            'summary': 'Asr Salaah',
            'start': {
                'dateTime': asr_datetime.isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': (asr_datetime + datetime.timedelta(minutes=15)).isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
        }
        calendar_service.events().insert(calendarId=CALENDAR_ID, body=asr_event).execute()

        # Create Maghreb event
        maghreb_event = {
            'summary': 'Maghreb Salaah',
            'start': {
                'dateTime': maghreb_datetime.isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': (maghreb_datetime + datetime.timedelta(minutes=15)).isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
        }
        calendar_service.events().insert(calendarId=CALENDAR_ID, body=maghreb_event).execute()

        # Create Isha event
        isha_event = {
            'summary': 'Isha Salaah',
            'start': {
                'dateTime': isha_datetime.isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': (isha_datetime + datetime.timedelta(minutes=15)).isoformat(),
                'timeZone': 'Africa/Johannesburg',
            },
        }
        calendar_service.events().insert(calendarId=CALENDAR_ID, body=isha_event).execute()

    print('Events created successfully!')

except HttpError as e:
    print(f'An error occurred: {e}')
