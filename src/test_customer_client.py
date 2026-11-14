from customer_client import CustomerClient


client = CustomerClient(
    "127.0.0.1",
    5001
)

print(
    client.login(
        "C005",
        "password123"
    )
)

print(
    client.get_account_balance(
        "A001"
    )
)

print(
    client.transfer(
        "A001",
        "127.0.0.1",
        5002,
        "BANK_GREECE",
        "A002",
        100
    )
)

print(
    client.get_account_balance(
        "A001"
    )
)