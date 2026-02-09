from app.services.auth_service import AuthService
from faker import Faker

fake = Faker()


def test_auth_service_registration(test_app):
    email = fake.email()
    password = fake.password()

    user_data = {"email": email, "password": password, "password_confirmation": password, "role": "customer"}
    result, status = AuthService.register_user(user_data)

    assert status == 201
    assert "data" in result
