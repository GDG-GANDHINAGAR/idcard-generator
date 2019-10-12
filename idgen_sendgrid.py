from __future__ import print_function
import json
import os
import base64
from io import BytesIO
import requests
import math
from PIL import Image, ImageDraw, ImageFont
import qrcode.image.svg
import qrcode
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from schedule_mail import mail_temp
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, Content

from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv('SG_APIKEY')
ORG_EMAIL = os.getenv('ORG_EMAIL')
ORG_NAME = os.getenv('ORG_NAME')
FONT = os.getenv('FONT')
# print(API_KEY)

sg = SendGridAPIClient(API_KEY)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID of spreadsheet : https://docs.google.com/spreadsheets/d/<THIS-PART-IS-ID>/edit#gid=0
SAMPLE_SPREADSHEET_ID = os.getenv('SHEET_ID')
SAMPLE_RANGE_NAME = 'A22:V'

def main():
    print("Getting data from the sheet...")
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # We can access the sheet values here
        print("Data received.")

        for row in values:
            reg_id = row[0]
            name = row[1] + ' ' + row[2]
            email = row[3]
            # designation = row[18]
            # inst = row[19]
            # org = row[21]

            # print('%s: Generating card for %s...' % (no, name))
            # no-=1
            # qr = qrcode.QRCode(
            #     version=1,
            #     error_correction=qrcode.constants.ERROR_CORRECT_M,
            #     box_size=10,
            #     border=2,
            # )
            # qr.add_data(reg_id)
            # qr.make(fit=True)
            # img = qr.make_image()

            # # Resize the QR code to 150px X 150px
            # img.thumbnail((221, 221), Image.ANTIALIAS)

            # img.save(os.path.join('qrcodes', email + '.png'))

            # template = Image.open('template.png')

            # # Paste QR code
            # template.paste(img, (205, 360))

            # # Write the name
            # draw = ImageDraw.Draw(template)
            # font = ImageFont.truetype(FONT, 55)

            # x, y = font.getsize(name)

            # draw.text(((321 - x / 2), (710 - y / 2)),
            #           name, font=font, fill='black')

            # # Write the designation
            # if designation != 'NA':
            #     draw = ImageDraw.Draw(template)
            #     font = ImageFont.truetype(FONT, 26)
            #     x, y = font.getsize(designation)
            #     draw.text(((321 - x / 2), (770 - y / 2)),
            #               designation, font=font, fill='black')

            # if org != 'NA':
            #     draw = ImageDraw.Draw(template)
            #     font = ImageFont.truetype(FONT, 30)
            #     x, y = font.getsize(org)

            #     draw.text(((321 - x / 2), (810 - y / 2)),
            #               org, font=font, fill='black')

            # elif inst != 'NA':
            #     draw = ImageDraw.Draw(template)
            #     font = ImageFont.truetype(FONT, 30)
            #     x, y = font.getsize(inst)

            #     draw.text(((321 - x / 2), (810 - y / 2)),
            #               inst, font=font, fill='black')

            # # Add abstract element
            # element = Image.open('element.png')
            # element.thumbnail((59, 59), Image.ANTIALIAS)
            # template.paste(element, (407, 557), element)
            # # Save the card
            # template.save(os.path.join('cards', email + '.png'))

            # buffer = BytesIO()
            # template.save(buffer, format="PNG")
            # base64Value = base64.b64encode(buffer.getvalue())

            message = Mail(
                from_email=(ORG_EMAIL, "GDG Gandhinagar"),
                subject="Schedule: DevFest Gandhinagar 2019",
                to_emails=[(email, name)],
                html_content=Content("text/html", mail_temp(name, email)))

            print("\tSending mail to " + name + "...")

            result = sg.client.mail.send.post(message.get())
            if result.status_code == 202:
                print("\t\tMail sent.")
            else:
                print("\t\tMail not sent.")

        print('All cards sent successfully.')


if __name__ == '__main__':
    main()
