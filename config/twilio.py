from twilio.rest import Client
import os

account_sid = os.getenv("SSID_TWILIO")
auth_token = os.getenv("AUTH_TOKEN_TWILIO")

def get_client():
    return Client(account_sid, auth_token)
