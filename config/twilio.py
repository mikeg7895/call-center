from twilio.rest import Client

account_sid = "AC049edd2bf0b498b15c43dbeb8b6a16e7"
auth_token = "f6c3dc956857d88de76edaf991e9617c"

def get_client():
    return Client(account_sid, auth_token)