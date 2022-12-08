import os
import locale
import base64
import subprocess
import mimetypes
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from settings import NAME, ADDRESS, SIGNATURE_PLACE, MAIL_FROM, MAIL_TO

from email.message import EmailMessage

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def send_notification(title: str, message: str):
    subprocess.Popen(["notify-send", title, message])


def fill_pdf(template_name: str, informations: dict, output_name: str):
    """Fill fields of template_name with informations dict and output a new pdf."""
    reader = PdfReader(template_name)
    writer = PdfWriter()
    page = reader.pages[0]
    writer.add_page(page)
    writer.update_page_form_field_values(writer.pages[0], informations)
    with open(output_name, "wb") as output_stream:
        writer.write(output_stream)


def gmail_send_message(**kwargs):
    """Create and send an email message
    Returns: message id
    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://mail.google.com/"]

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    body = kwargs.get("body")
    subject = kwargs.get("subject")
    sender = kwargs.get("sender")
    receiver = kwargs.get("receiver")
    filename = kwargs.get("filename")

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(body)

        message["To"] = receiver
        message["From"] = sender
        message["Subject"] = subject

        attachment_filename = filename
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")

        with open(attachment_filename, "rb") as fp:
            attachment_data = fp.read()
        message.add_attachment(
            attachment_data, maintype, subtype, filename=attachment_filename
        )

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            "raw": encoded_message,
        }
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
    return send_message.get("id")


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    current_date = datetime.now().strftime("%d/%m/%Y")
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().strftime("%Y")

    informations = {
        "name": NAME,
        "address": ADDRESS,
        "date": current_date,
        "month": current_month,
        "signature_place": SIGNATURE_PLACE,
        "signature": NAME.upper(),
    }
    fill_pdf(
        "declaration_transport_template.pdf", informations, "declaration_transport.pdf"
    )
    subject = f"Attestation transport mobilités durables {current_month} {current_year}"
    body = f"""
    Bonjour,

    Vous trouverez en pièce jointe mon attestation de transport pour {current_month}.

    Bonne fin de journée !

    {NAME}
    """
    message_id = gmail_send_message(
        body=body,
        subject=subject,
        sender=MAIL_FROM,
        receiver=MAIL_TO,
        filename="declaration_transport.pdf",
    )

    if message_id:
        notification_message = "Mail envoyé avec succès."
    else:
        notification_message = "Echec de l'envoi du mail."

    notification_title = "Cron task: déclaration transport"

    send_notification(notification_title, notification_message)