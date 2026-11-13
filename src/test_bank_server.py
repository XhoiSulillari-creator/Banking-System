from bank import Bank
from bank_server import BankServer
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from authentication import AuthenticationService
from customer import Customer


# -------------------------
# Bank Albania
# -------------------------

customer_repository_1 = CustomerRepository(
    "data/bank1_customers.json"
)

account_repository_1 = AccountRepository(
    "data/bank1_accounts.json",
    customer_repository_1
)

authentication_service_1 = AuthenticationService()

bank1 = Bank(
    "Bank Albania",
    customer_repository_1,
    account_repository_1,
    authentication_service_1
)

customer1 = Customer("C005", "Xhoi")

bank1.add_customer(customer1)

bank1.register_customer_credentials(
    "C005",
    "password123"
)


# -------------------------
# Bank Greece
# -------------------------

customer_repository_2 = CustomerRepository(
    "data/bank2_customers.json"
)

account_repository_2 = AccountRepository(
    "data/bank2_accounts.json",
    customer_repository_2
)

authentication_service_2 = AuthenticationService()

bank2 = Bank(
    "Bank Greece",
    customer_repository_2,
    account_repository_2,
    authentication_service_2
)

customer2 = Customer("C006", "Alice")

bank2.add_customer(customer2)

bank2.register_customer_credentials(
    "C006",
    "alice123"
)


# -------------------------
# Start Bank Albania server
# -------------------------

server = BankServer(
    bank1,
    "127.0.0.1",
    5001
)

server.start()