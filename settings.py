import os
from dotenv import load_dotenv

load_dotenv()

NAME = os.environ.get("NAME")
ADDRESS = os.environ.get("ADDRESS")
SIGNATURE_PLACE = os.environ.get("SIGNATURE_PLACE")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_TO = os.environ.get("MAIL_TO")
