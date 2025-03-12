from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import csv

def get_form_answers_dictionary():
    # Get credentials from environment variable
    google_credentials = os.getenv('GOOGLE_CREDENTIALS')
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # Parse the credentials JSON string
    credentials_info = json.loads(google_credentials)
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=scopes
    )

    # Build the service object
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    range_name = "Form Responses 1"

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get("values", [])

    # Convert to dictionary
    data = None
    if values:
        headers = values[0]
        data = [dict(zip(headers, row)) for row in values[1:]]

    # Return None if no answers, or a dictionary with all info if there are answers
    return data

def export_form_data_to_csv(header_name, header_email):
    # Get data from the forms as a dictionary
    data = get_form_answers_dictionary()

    # Export data to CSV in the right format (ID, Name, Email), each row a new response
    with open('Coffee Partner Lottery participants.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', header_name, header_email])
        for i, response in enumerate(data):
            writer.writerow([i+1, response['What is your full name?'], response['What is your email adress?']])

