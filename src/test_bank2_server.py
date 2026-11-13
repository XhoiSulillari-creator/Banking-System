from bank import Bank
from bank_server import BankServer
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from authentication import AuthenticationService
from customer import Customer


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

bank.register_customer_credentials(
    "C006",
    "alice123"
)

server = BankServer(
    bank,
    "127.0.0.1",
    5002
)

server.start()