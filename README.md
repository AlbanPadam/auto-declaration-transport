# auto-declaration-transport
Automate filling declaration of transport, send it as an attachment in gmail.

## User guide (Linux)
### Setup
- Clone this repository
- `python -m venv .venv ` (Create a virtual environment)
- `source .venv/bin/activate` (Activate it)
- `pip install -r requirements.txt` (Install requirements)

### Gmail API
Please make sure you are signed in to gmail before following those steps
- [Create a project](https://console.cloud.google.com/projectcreate) 
- Setup
- [Enable GMAIL API in your project](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com)
- Go on [Consent](https://console.cloud.google.com/apis/credentials/consent?)
    - choose intern usage
    - fill in your email when needed
    - leave others boxes as default
- Go on [Credentials](https://console.cloud.google.com/apis/credentials) and make sure your project is selected (top right)
    - Click Create Credentials > OAuth client ID.
    - Click Application type > Desktop app.
    - In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
    - Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
    - Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
- Save the downloaded JSON file as credentials.json, and move it in the root directory.

### Customize your informations
- Create a .env file in the root directory and fills it in:
~~~
NAME = 
ADDRESS = 
SIGNATURE_PLACE = 
MAIL_FROM = 
MAIL_TO = 
~~~
