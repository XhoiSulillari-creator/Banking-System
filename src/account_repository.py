import json
from account import Account
from customer_repository import CustomerRepository


class AccountRepository:
    def __init__(self, file_path, customer_repository):
        self.file_path = file_path
        self.customer_repository = customer_repository

    def save(self, account):
        accounts = self._load_all()

        data = {
            "account_id": account.account_id,
            "customer_id": account.owner.customer_id,
            "balance": account.balance
        }

        accounts.append(data)

        with open(self.file_path, "w") as file:
            json.dump(accounts, file, indent=4)

    def load(self, account_id):
        accounts = self._load_all()

        for data in accounts:
            customer = self.customer_repository.load(
                data["customer_id"]
            )

            if customer is None:
                continue

            if data["account_id"] == account_id:
                return Account(
                    data["account_id"],
                    customer,
                    data["balance"]
                )

        return None

    def _load_all(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []