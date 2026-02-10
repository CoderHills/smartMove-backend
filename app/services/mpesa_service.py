import requests
import base64
from datetime import datetime
from flask import current_app
from requests.auth import HTTPBasicAuth


class MpesaService:
    @staticmethod
    def get_token():
        url = f"{current_app.config['MPESA_BASE_URL']}/oauth/v1/generate?grant_type=client_credentials"
        resp = requests.get(
            url,
            auth=HTTPBasicAuth(
                current_app.config["MPESA_CONSUMER_KEY"],
                current_app.config["MPESA_CONSUMER_SECRET"],
            ),
        )
        return resp.json().get("access_token")

    @staticmethod
    def stk_push(phone, amount, booking_id):
        token = MpesaService.get_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{current_app.config['MPESA_SHORTCODE']}{current_app.config['MPESA_PASSKEY']}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": current_app.config["MPESA_SHORTCODE"],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": current_app.config["MPESA_SHORTCODE"],
            "PhoneNumber": phone,
            "CallBackURL": current_app.config["CALLBACK_URL"],
            "AccountReference": f"SMOVE-{booking_id}",
            "TransactionDesc": "Payment for Smartmove",
        }

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{current_app.config['MPESA_BASE_URL']}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )
        return response.json()
