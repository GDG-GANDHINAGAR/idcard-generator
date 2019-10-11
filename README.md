# ID Generator for DevFest

This similar code can be used further for certificate generation also.

## How to Use 😕

### Get your `credentials.json` file

Visit [this](https://developers.google.com/sheets/api/quickstart/python) and click on the 'Enable the Google Sheets API' to enable sheets API for your account, and get your `credentials.json` file.

### Install pipenv

Use the command

```sh
sudo -H pip install pipenv
```

and then simply setup pipenv

```sh
pipenv install
```

and activate pipenv shell using

```sh
pipenv shell
```

### Create folders if not already

```sh
    mkdir cards
    mkdir qrcodes
```

### Add a `.env` file with Mailjet credentials and Google Sheet ID

Create a `.env` file in the root directory of your project, and add the following variables:

```env
FONT=<FONT-FILE-NAME>
SHEET_ID=<YOUR-GOOGLE-SHEET-ID>
ORG_EMAIL=<ORG-EMAIL>
ORG_NAME=<ORG-NAME>
MJ_APIKEY_PUBLIC=<YOUR-MAILJET-PUBLIC-KEY>
MJ_APIKEY_PRIVATE=<YOUR-MAILJET-PRIVATE-KEY>
SG_APIKEY=<YOUR-SENDGRID-API-KEY>
```

Now simply run:

```sh
    python idgen.py
```

## Makers 🛠

- Code by Jay Mistry [@rossoskull](https://github.com/rossoskull)
- Designs by Pranay Agarwal [pydesigns](https://www.behance.net/pydesigns)
