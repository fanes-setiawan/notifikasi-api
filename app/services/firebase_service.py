import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests


load_dotenv()

# Ambil string kredensial JSON dari .env
credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

if credentials_json:
    # Parsing string JSON menjadi dictionary
    credentials_dict = json.loads(credentials_json)  # Mengubah JSON string ke dictionary
    
    # Menggunakan credentials_dict untuk membuat kredensial dari service account
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
else:
    raise ValueError("Kredensial Firebase tidak ditemukan. Pastikan file .env sudah diatur.")


# Fungsi untuk mendapatkan access token Firebase
def get_firebase_access_token():
    try:
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )
        print("Credentials:", credentials)
        request = Request()
        credentials.refresh(request)
        return credentials.token
    except Exception as e:
        raise Exception(f"Error getting access token: {str(e)}")

# Fungsi untuk mengirimkan notifikasi ke FCM
def send_firebase_notification(token: str, title: str, body: str, data: dict):
    try:
        access_token = get_firebase_access_token()
        print("Access token:", access_token)
        url = "https://fcm.googleapis.com/v1/projects/hydsmartfire/messages:send"

        payload = {
            "message": {
                "token": token,
                "notification": {"title": title, "body": body},
                "data": data,
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Firebase error: {response.status_code}, {response.text}")
    except Exception as e:
        raise Exception(f"Error sending notification: {str(e)}")