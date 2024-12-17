from twilio.rest import Client

account_sid = "************************"
auth_token = "*************************"

def get_client():
    return Client(account_sid, auth_token)
