from flask import Blueprint, request
from app.services.mpesa_service import MpesaService
from app.utils.response import success, error

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/stk-push", methods=["POST"])
def initiate_payment():
    data = request.get_json()
    # Trigger the prompt
    response = MpesaService.stk_push(data["phone"], data["amount"], data["booking_id"])
    return success(data=response, message="STK Push Initiated")


@payment_bp.route("/callback", methods=["POST"])
def payment_callback():
    # This is where M-Pesa sends the results (Success/Fail)
    data = request.get_json()
    result_code = data["Body"]["stkCallback"]["ResultCode"]
    # Add logic here to update your 'Booking' table in the database
    return success(message="Callback processed")
