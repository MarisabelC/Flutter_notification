import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def get_device_tokens():
    global deviceTokens
    cred = credentials.Certificate('service_account_key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection(u'tokens')
    docs = users_ref.stream()
    deviceTokens = []
    for doc in docs:
        deviceTokens.append(doc.to_dict()['token'])
    return deviceTokens

def send_notification():
    device_tokens = get_device_tokens()
    server_token = 'server token'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + server_token,
    }
    for deviceToken in device_tokens:
        body = {
            'notification': {'title': 'notification title.',
                             'body': 'notification body. '
                             },
            'to':
                deviceToken,
            'priority': 'high',
            #   'data': dataPayLoad,
        }
        response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        print(response.status_code)

        print(response.json())


if __name__ == "__main__":
    send_notification()

