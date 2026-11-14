from admin_authentication import AdminAuthenticationService
from authentication import AuthenticationService


def test_admin_otp_is_single_use():
    service = AdminAuthenticationService(
        "data/test_admin_mailbox.json"
    )

    otp = service.request_otp("TEST_ADMIN")

    assert service.authenticate(
        "TEST_ADMIN",
        otp
    ) is True

    assert service.authenticate(
        "TEST_ADMIN",
        otp
    ) is False


def test_admin_wrong_otp_fails():
    service = AdminAuthenticationService(
        "data/test_admin_mailbox.json"
    )

    service.request_otp("TEST_ADMIN")

    assert service.authenticate(
        "TEST_ADMIN",
        "000000"
    ) is False


def test_customer_authentication():
    authentication_service = AuthenticationService()

    authentication_service.register(
        "TEST001",
        "password123"
    )

    assert authentication_service.authenticate(
        "TEST001",
        "password123"
    ) is True

    assert authentication_service.authenticate(
        "TEST001",
        "wrongpassword"
    ) is False


def test_customer_wrong_password():
    authentication_service = AuthenticationService()

    authentication_service.register(
        "TEST002",
        "correctpassword"
    )

    assert authentication_service.authenticate(
        "TEST002",
        "wrongpassword"
    ) is False


def test_admin_wrong_id_fails():
    service = AdminAuthenticationService(
        "data/test_admin_mailbox.json"
    )

    otp = service.request_otp("TEST_ADMIN")

    assert service.authenticate(
        "WRONG_ADMIN",
        otp
    ) is False