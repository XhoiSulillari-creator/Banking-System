from account import Account
from customer import Customer
from account_repository import AccountRepository
from customer_repository import CustomerRepository

customer = Customer("C001", "Alice")

account = Account("A001", customer, 1000)

customer_repository = CustomerRepository("data/customers.json")
account_repository = AccountRepository(
    "data/accounts.json",
    customer_repository
)

customer_repository.save(customer)
account_repository.save(account)

loaded_account = account_repository.load("A001")

print(loaded_account.account_id)
print(loaded_account.owner.name)
print(loaded_account.balance)