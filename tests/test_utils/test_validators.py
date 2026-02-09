from app.utils.validators import is_valid_kenyan_phone, is_valid_email


def test_validators():
    assert is_valid_kenyan_phone("0712345678") is True
    assert is_valid_kenyan_phone("12345") is False
    assert is_valid_email("alvin@smart.com") is True
    assert is_valid_email("invalid-email") is False
