# ID Generator for DevFest '19

This similar code can be used further for certificate generation also.

## How to Use

### Get your `credentials.json` file

Visit [this](https://developers.google.com/sheets/api/quickstart/python) and click on the 'Enable the Google Sheets API' to enable sheets API for your account, and get your `credentials.json` file.

### Install Sheets pip module

Run the following command to install the Google Sheets module

```sh
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Install `qrcode` for QR code generation

Run the following command

```sh
    pip install qrcode[pil] qrcode
```

Now simply run:

```sh
    python idgen.py
```

## Makers

- Code by Jay Mistry [@rossoskull](https://github.com/rossoskull)
- Designs by Pranay Agarwal [pydesigns](https://www.behance.net/pydesigns)
