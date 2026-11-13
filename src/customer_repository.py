import json#converting our Python dictionary into JSON that can be stored in a file
from customer import Customer

class CustomerRepository:
    def __init__(self,file_path):
        self.file_path = file_path

    def save(self, customer):
        customers = self._load_all()

        data = {
            "customer_id": customer.customer_id,
            "name": customer.name
    }

        customers.append(data)

        with open(self.file_path, "w") as file:
            json.dump(customers, file, indent=4)

    def load(self, customer_id):
        customers = self._load_all()

        for data in customers:
            if data["customer_id"] == customer_id:
                return Customer(data["customer_id"], data["name"])

        return None

    def _load_all(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []