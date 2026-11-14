from bank import Bank
from bank_server import BankServer
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from authentication import AuthenticationService
from server_authentication import ServerAuthenticationService
from customer import Customer
from account import Account


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

account = Account(
    "A001",
    customer,
    1000
)

bank.add_account(account)

server_authentication_service = ServerAuthenticationService()

server_authentication_service.register(
    "BANK_ALBANIA",
    "alb-server-123"
)

server_authentication_service.register(
    "BANK_GREECE",
    "gr-server-123"
)

server = BankServer(
    bank,
    "127.0.0.1",
    5001,
    server_authentication_service,
    "BANK_ALBANIA"
)

success = server.execute_interbank_transfer(
    "127.0.0.1",
    5002,
    "BANK_GREECE",
    "alb-server-123",
    "A001",
    "A002",
    200
)

print(f"Inter-bank transfer successful: {success}")

print(
    f"Bank Albania A001: "
    f"{bank.get_account('A001').balance}"
)