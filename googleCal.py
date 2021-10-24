from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

scopes = ["https://www.googleapis.com/auth/calendar.events"]
flow = InstalledAppFlow.from_client_secrets_file("./app/client_secret.json", scopes=scopes)
creds = flow.run_local_server(port=0)

service = build('calendar', 'v3', credentials=creds)

startTime = startTime = datetime.strptime("2021-10-22 5:00", '%Y-%m-%d %H:%M')
endTime = startTime + timedelta(minutes=45)

event = {
  'summary': 'Appointment',
  'description': 'Appointment',
  'start': {
    'dateTime': startTime,
    'timeZone': 'Asia/Kolkata',
  },
  'end': {
    'dateTime': endTime,
    'timeZone': 'Asia/Kolkata',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=1'
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print(event.get('htmlLink'))