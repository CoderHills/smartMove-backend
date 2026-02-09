from app.services.auth_service import AuthService
from faker import Faker

fake = Faker()


def test_auth_service_registration(app):
    email = fake.email()
    password = fake.password()

    result, status = AuthService.register_user(email, password)

    assert status == 201
    assert "data" in result
