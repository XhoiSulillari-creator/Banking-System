class Transaction:
    def __init__(self, transaction_id, source_account, destination_account, amount):
        self.transaction_id = transaction_id
        self.source_account = source_account
        self.destination_account = destination_account
        self.amount = amount

    def execute(self):
        withdraw_success = self.source_account.withdraw(self.amount)
        if not withdraw_success:
           return False

        deposit_success = self.source_account.deposit(self.amount)
        if deposit_success:
            return True

        self.source_account.deposit(self.amount)
        return False