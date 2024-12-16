from twilio.rest import Client

account_sid = "AC049edd2bf0b498b15c43dbeb8b6a16e7"
auth_token = "f2254ad50d057dde3ab757a1d94c3549"

def get_client():
    return Client(account_sid, auth_token)