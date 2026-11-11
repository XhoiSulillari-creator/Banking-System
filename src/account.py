class Account:
    def __init__(self,account_id,owner,balance):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
    def deposit(self,amount):
        if(amount>0):
            self.balance = self.balance + amount
            return True
        else:
            return False
    def withdraw(self,amount):
        if(self.balance>=amount and amount>0):
            self.balance = self.balance - amount
            return True
        else:
            return False
