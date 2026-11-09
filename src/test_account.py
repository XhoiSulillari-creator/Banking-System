from account import Account
account = Account(1001,"Alice",1000)
account.deposit(500)
account.withdraw(300)
print(account.balance)

class Dog:
    def __init__(self,name):
        self.name = name
class Person:
    def __init__(self,name):
        self.name = name
        self.dogs = []

person = Person("Alice")
person.dogs.append(Dog("lexi"))

