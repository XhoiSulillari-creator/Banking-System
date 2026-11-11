import json
from account import Account
from customer_repository import CustomerRepository

class AccountRepository:
    def __init__(self, file_path, customer_repository):
        self.file_path = file_path
        self.customer_repository = customer_repository
    
    def save(self,account):
        data = {
    "account_id": account.account_id,
    "customer_id": account.owner.customer_id,
    "balance": account.balance
}
        with open(self.file_path, "w") as file:
            json.dump(data, file)#take the "data" and write it into the json

    def load(self, account_id):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        customer = self.customer_repository.load(data["customer_id"])

        if customer is None:
            return None

        if data["account_id"] == account_id:
            return Account(
                data["account_id"],
                customer,
                data["balance"]
            )

        return None