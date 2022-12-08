# :bike: auto-declaration-transport :bike:
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

### Run script once to prompt a google authentication (Set MAIL_TO to your address for this :p)
- `python send_transport_certificate.py`
- This authentication should be made once and provides you a token that is valid for a long time (1 year)
- You should see a notification telling you that the mail was successfully send

### Automate script
We will use a cron for this. Note that your computer need to be on at execution time otherwise the task won't complete.
- Verify your .env variables are correctly set
- crontab -e
- Write in the editor (modify PATH_TO_YOUR_FOLDER accordingly)
~~~
0 14 20 * * source PATH_TO_YOUR_FOLDER/.venv/bin/activate; python send_transport_certificate.py
~~~

This will run the script every 20th day of every month at 14:00. See [crontab guru](https://crontab.guru/) to set the execution timing of your cron.
