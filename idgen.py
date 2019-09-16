from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Import QR code stuff
import qrcode
import qrcode.image.svg

# Import PIL stuff
from PIL import Image, ImageDraw, ImageFont
import math

import requests
from io import BytesIO

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.

# ID of spreadsheet : https://docs.google.com/spreadsheets/d/<THIS-PART-IS-ID>/edit#gid=0
SAMPLE_SPREADSHEET_ID = '1tnjNRDMcbPherAWI-pqDkRnhmcI9ClrBVfCHNokE9dg'
SAMPLE_RANGE_NAME = 'A1:D'


def main():
    print("Getting data from the sheet...")

    """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
            name = row[0]
            contact = row[1]
            role = row[2]
            imageUrl = row[3]

            print('Generating card for %s...' % (name))

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )

            # QR Code factory
            # factory = qrcode.image.svg.SvgPathImage

            data = '%s %s %s' % (name, contact, role)

            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()

            # Resize the QR code to 150px X 150px
            img.thumbnail((221, 221), Image.ANTIALIAS)

            img.save(os.path.join('qrcodes', contact + '.png'))
            # Image.open(code).save(os.path.join('qrcodes', contact + '.svg'))

            template = Image.open('template.png')

            # Paste QR code
            template.paste(img, (208, 680))

            # Write the name
            draw = ImageDraw.Draw(template)
            font = ImageFont.truetype('Product-Sans-Regular.ttf', 55)

            x, y = font.getsize(name)

            draw.text(((321 - x / 2), (631 - y / 2)),
                      name, font=font, fill='black')

            # Get and paste the profile picture
            print('\tGetting profile picture...')
            imageResponse = requests.get(imageUrl)
            profileImage = Image.open(BytesIO(imageResponse.content))

            profileImage.thumbnail((288, 288), Image.ANTIALIAS)

            # Make the image a circle
            bigsize = (profileImage.size[0] * 3, profileImage.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            maskDraw = ImageDraw.Draw(mask)
            maskDraw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(profileImage.size, Image.ANTIALIAS)
            profileImage.putalpha(mask)

            template.paste(profileImage, (175, 282), profileImage)

            # Add abstract element
            element = Image.open('element.png')
            element.thumbnail((59, 59), Image.ANTIALIAS)
            template.paste(element, (397, 507), element)
            # Save the card
            template.save(os.path.join('cards', contact + '.png'))

        print('All cards printed successfully.')


if __name__ == '__main__':
    main()
# [END sheets_quickstart]
