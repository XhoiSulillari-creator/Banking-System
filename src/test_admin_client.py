from admin_client import AdminClient


client = AdminClient(
    "127.0.0.1",
    5001
)

admin_id = "ADMIN001"

otp = client.request_otp(admin_id)

print(f"OTP received: {otp}")

print(
    client.login(
        admin_id,
        otp
    )
)

print(
    client.get_account("A001")
)

print(
    client.get_statistics()
)