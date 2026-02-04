import uuid
from datetime import datetime


def generate_unique_id():
    return str(uuid.uuid4())


def generate_booking_ref():
    """Generates a short human-readable reference (e.g., SM-2024-X89)"""
    year = datetime.now().year
    random_part = str(uuid.uuid4()).upper()[:4]
    return f"SM-{year}-{random_part}"


def format_currency(amount):
    return f"KES {amount:,.2f}"
