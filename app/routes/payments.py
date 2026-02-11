from flask import Blueprint, request, current_app
from app.services.mpesa_service import MpesaService
from app.utils.response import success, error_response as error
from app.models.booking import Booking, PaymentStatus # Import Booking and PaymentStatus
from app.extensions import db # Import db for database operations

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/stk-push", methods=["POST"])
def initiate_payment():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")
    booking_id = data.get("booking_id")

    if not all([phone, amount, booking_id]):
        return error("Missing required fields: phone, amount, booking_id", 400)

    booking = Booking.query.get(booking_id)
    if not booking:
        return error("Booking not found", 404)

    # Trigger the prompt
    response = MpesaService.stk_push(phone, amount, booking_id)

    # Check if STK Push was successful
    if response.get("ResponseCode") == "0":
        booking.checkout_request_id = response.get("CheckoutRequestID")
        booking.payment_status = PaymentStatus.PENDING # Set payment status to pending
        db.session.commit()
        return success(data=response, message="STK Push Initiated Successfully")
    else:
        return error("STK Push Initiation Failed", status_code=400)


@payment_bp.route("/callback", methods=["POST"])
def payment_callback():
    # This is where M-Pesa sends the results (Success/Fail)
    data = request.get_json()
    
    # Extract relevant fields
    result_code = data["Body"]["stkCallback"]["ResultCode"]
    checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    
    mpesa_receipt_number = None
    amount = None

    # CallbackMetadata might not be present for failed transactions
    callback_metadata_items = data["Body"]["stkCallback"].get("CallbackMetadata", {}).get("Item", [])
    
    for item in callback_metadata_items:
        if item["Name"] == "MpesaReceiptNumber":
            mpesa_receipt_number = item["Value"]
        elif item["Name"] == "Amount":
            amount = item["Value"]

    booking = Booking.query.filter_by(checkout_request_id=checkout_request_id).first()

    if booking:
        if result_code == 0: # Successful transaction (integer 0)
            booking.mpesa_receipt_number = mpesa_receipt_number
            booking.payment_status = PaymentStatus.COMPLETED
        else: # Failed or cancelled transaction
            booking.payment_status = PaymentStatus.FAILED
        db.session.commit()
    else:
        # Log an error if booking not found for a callback
        current_app.logger.error(f"Booking not found for CheckoutRequestID: {checkout_request_id}")

    return success(message="Callback processed")
