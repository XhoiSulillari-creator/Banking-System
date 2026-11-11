import json#converting our Python dictionary into JSON that can be stored in a file
from customer import Customer

class CustomerRepository:
    def __init__(self,file_path):
        self.file_path = file_path

    def save(self,customer):
        data = {
            "customer_id": customer.customer_id,
            "name": customer.name
        }
        with open(self.file_path,"w")as file:
            json.dump(data,file)

    def load(self, customer_id):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        if data["customer_id"] == customer_id:
            return Customer(data["customer_id"], data["name"])

        return None   