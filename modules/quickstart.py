# !/usr/bin/env python3

# quickstart.py
# Bix 1/30/19
# quickstart

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pandas as pd
import csv

class Quickstart:
    """Quickstart Class"""

    def __init__(self, date_in):
        self.DATE = date_in
        self.str_rfv_merged_rgx = ''
        with open('output/'+self.DATE+'_rfv-merged-rgx.csv') as file:
            csv_reader = csv.reader(file, delimiter=',',quotechar='|')
            for row in csv_reader:
                row = ','.join(row)
                index = row.find(',')
                self.str_rfv_merged_rgx += row[index+1:] + '\n'

        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = 'spreadsheetID'


    def main(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('config/token_google.pickle'):
            with open('config/token_google.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials_google.json', self.SCOPES)
                self.creds = self.flow.run_local_server()
            # Save the credentials for the next run
            with open('config/token_google.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)

        self.request = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID)
        self.response = self.request.execute()
        self.sheets = self.response.get('sheets','')
        self.sheet_id_to_del = None
        for i in range(len(self.sheets)):
            title = self.sheets[i].get("properties", {}).get("title", "Sheet1")
            sheet_id = self.sheets[i].get("properties", {}).get("sheetId", 0)
            if title == self.DATE:
                self.sheet_id_to_del = sheet_id
                break

        self.batch_update_spreadsheet_request_body = None

        if self.sheet_id_to_del == None:
            self.batch_update_spreadsheet_request_body = {
            # A list of updates to apply to the spreadsheet.
            # Requests will be applied in the order they are specified.
            # If any request is not valid, no requests will be applied.
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": self.DATE,
                            "index": 0,
                            "gridProperties": {
                                "rowCount": 50,
                                "columnCount": 10,
                                "frozenRowCount": 1
                            },
                            "tabColor": {
                                "red": 1.0,
                                "green": 0.6,
                                "blue": 0.0
                            }
                        }
                    }
                },
            ], 
            }
        else:
            self.batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteSheet": {
                        "sheetId": self.sheet_id_to_del
                    }

                },
                {
                    "addSheet": {
                        "properties": {
                            "title": self.DATE,
                            "index": 0,
                            "gridProperties": {
                                "rowCount": 50,
                                "columnCount": 10,
                                "frozenRowCount": 1
                            },
                            "tabColor": {
                                "red": 1.0,
                                "green": 0.6,
                                "blue": 0.0
                            }
                        }
                    }
                },
            ], 
            }


        self.request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=self.batch_update_spreadsheet_request_body)
        self.response = self.request.execute()
        print(self.response)
        if self.sheet_id_to_del == None:
            print(self.response['replies'][0]['addSheet'])
            self.sheetId_new = self.response['replies'][0]['addSheet']['properties']['sheetId']
        else:
            print(self.response['replies'][1]['addSheet'])
            self.sheetId_new = self.response['replies'][1]['addSheet']['properties']['sheetId']

        self.batch_update_spreadsheet_request_body = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheetId_new,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.0,
                                "green": 0.0,
                                "blue": 0.4
                            },
                            "horizontalAlignment" : "CENTER",
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 1.0,
                                    "green": 1.0,
                                    "blue": 1.0
                                },
                                "fontSize": 12,
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            },
            {
                "pasteData": {
                    "coordinate": {
                        "sheetId": self.sheetId_new,
                        "rowIndex": 0,
                        "columnIndex": 0
                    },
                    "data": self.str_rfv_merged_rgx,
                    "type": "PASTE_NORMAL",

                    "delimiter": ",",
                    # "html": False
                }
            },
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": self.sheetId_new,
                        "dimension": "COLUMNS",
                        "startIndex": 0
                    }
                }
            }
        ],
        }

        self.request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=self.batch_update_spreadsheet_request_body)
        self.response = self.request.execute()
        print(self.response)