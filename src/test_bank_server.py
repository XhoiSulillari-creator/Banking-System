from bank import Bank
from bank_server import BankServer
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from authentication import AuthenticationService
from server_authentication import ServerAuthenticationService
from customer import Customer


# -------------------------
# Bank Albania
# -------------------------

customer_repository = CustomerRepository(
    "data/bank1_customers.json"
)

account_repository = AccountRepository(
    "data/bank1_accounts.json",
    customer_repository
)

authentication_service = AuthenticationService()

bank = Bank(
    "Bank Albania",
    customer_repository,
    account_repository,
    authentication_service
)

customer = Customer("C005", "Xhoi")

bank.add_customer(customer)

bank.register_customer_credentials(
    "C005",
    "password123"
)


# -------------------------
# Server authentication
# -------------------------

server_authentication_service = ServerAuthenticationService()

server_authentication_service.register(
    "BANK_ALBANIA",
    "alb-server-123"
)

server_authentication_service.register(
    "BANK_GREECE",
    "gr-server-123"
)


# -------------------------
# Bank Albania server
# -------------------------

server = BankServer(
    bank,
    "127.0.0.1",
    5001,
    server_authentication_service,
    "BANK_ALBANIA"
)

server.start()