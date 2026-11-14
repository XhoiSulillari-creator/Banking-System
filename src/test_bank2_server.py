from bank import Bank
from bank_server import BankServer
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from authentication import AuthenticationService
from server_authentication import ServerAuthenticationService
from customer import Customer
from account import Account
from admin_authentication import AdminAuthenticationService


# -------------------------
# Bank Greece
# -------------------------

customer_repository = CustomerRepository(
    "data/bank2_customers.json"
)

account_repository = AccountRepository(
    "data/bank2_accounts.json",
    customer_repository
)

authentication_service = AuthenticationService()

bank = Bank(
    "Bank Greece",
    customer_repository,
    account_repository,
    authentication_service
)

customer = Customer("C006", "Alice")

bank.add_customer(customer)

account = Account(
    "A002",
    customer,
    500
)

bank.add_account(account)

bank.register_customer_credentials(
    "C006",
    "alice123"
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
# Bank Greece server
# -------------------------

admin_authentication_service = AdminAuthenticationService(
    "data/bank2_admin_mailbox.json"
)

server = BankServer(
    bank,
    "127.0.0.1",
    5002,
    server_authentication_service,
    "BANK_GREECE",
    admin_authentication_service
)

server.start()