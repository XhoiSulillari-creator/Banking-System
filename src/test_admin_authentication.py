from admin_authentication import AdminAuthenticationService


service = AdminAuthenticationService(
    "data/admin_mailbox.json"
)

otp = service.request_otp("ADMIN001")

print(f"Generated OTP: {otp}")

print(
    "First authentication:",
    service.authenticate(
        "ADMIN001",
        otp
    )
)

print(
    "Second authentication:",
    service.authenticate(
        "ADMIN001",
        otp
    )
)

print(
    "Wrong OTP:",
    service.authenticate(
        "ADMIN001",
        "000000"
    )
)