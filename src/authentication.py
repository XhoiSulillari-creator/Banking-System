class AuthenticationService:
    def __init__(self):
        self.credentials = {}

    def register(self, customer_id, password):
        self.credentials[customer_id] = password

    def authenticate(self, customer_id, password):
        if customer_id not in self.credentials:
            return False

        return self.credentials[customer_id] == password