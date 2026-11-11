from account import Account
from transaction import Transaction
from customer import Customer

customer = Customer("C001", "Alice")

acc1 = Account("A001", customer, 1000)
acc2 = Account("A002", customer, 500)

transaction = Transaction("T001", acc1, acc2, 200)

result = transaction.execute()
print(result)
print(acc1.balance)
print(acc2.balance)