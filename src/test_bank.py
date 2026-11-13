from bank import Bank
from customer_repository import CustomerRepository
from account_repository import AccountRepository
from customer import Customer
from account import Account
from authentication import AuthenticationService


authentication_service = AuthenticationService()
customer_repository = CustomerRepository("data/customers.json")
account_repository = AccountRepository(
    "data/accounts.json",
    customer_repository
)

bank = Bank(
    "Bank Albania",
    customer_repository,
    account_repository,
    authentication_service
)

customer1 = Customer("C005", "Xhoi")
customer2 = Customer("C006", "Alice")

account1 = Account("A001", customer1, 1000)
account2 = Account("A002", customer2, 500)

customer_repository.save(customer1)
customer_repository.save(customer2)

account_repository.save(account1)
account_repository.save(account2)

print(bank.name)

print(bank.get_customer("C005").name)
print(account_repository.load("A001"))
print(customer_repository.load("C005"))
print(bank.get_account("A001").balance)
print(bank.get_account("A002").balance)

success = bank.transfer(
    "T001",
    "A001",
    "A002",
    200
)

print("Transfer successful:", success)

print("A001 balance:", bank.get_account("A001").balance)
print("A002 balance:", bank.get_account("A002").balance)

print(bank.register_customer_credentials("C005", "password123"))


print(bank.authenticate_customer("C005", "password123"))
print(bank.authenticate_customer("C005", "wrongpassword"))