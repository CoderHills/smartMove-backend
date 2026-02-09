from app.utils.validators import Validator


def test_validators():
    assert Validator.is_valid_email("alvin@smart.com") is True
    assert Validator.is_valid_email("invalid-email") is False