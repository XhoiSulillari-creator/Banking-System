class Account:
    def __init__(self,account_id,owner,balance):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
    def deposit(self,amount):
        self.balance = self.balance + amount
    def withdraw(self,amount):
        if(self.balance>=amount):
            self.balance = self.balance - amount
        else:
            print("Insufficient funds")