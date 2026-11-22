from command import Command


class LoginCommand(Command):

    def __init__(self, bank_server, message):
        self.bank_server = bank_server
        self.message = message

    def execute(self):
        return self.bank_server._handle_customer_login(
            self.message
        )