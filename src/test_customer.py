from account import Account
from customer import Customer

customer = Customer("C001","Alice")
account = Account("A001",customer,1000)
account1 = Account("A002",customer,5000)

customer.add_account(account)
customer.add_account(account1)

print(customer.accounts[0].account_id)
print(customer.accounts[0].owner.name)
print(customer.accounts[0].balance)
print(customer.accounts)
print(len(customer.accounts))