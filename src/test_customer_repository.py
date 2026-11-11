from customer import Customer
from customer_repository import CustomerRepository

customer = Customer("C001", "Alice")
repository = CustomerRepository("data/customers.json")

repository.save(customer)

loaded_customer = repository.load("C001")

print(loaded_customer.customer_id)
print(loaded_customer.name)