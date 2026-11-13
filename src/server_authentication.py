class ServerAuthenticationService:
    def __init__(self):
        self.credentials = {}

    def register(self, server_id, credential):
        self.credentials[server_id] = credential

    def authenticate(self, server_id, credential):
        if server_id not in self.credentials:
            return False

        return self.credentials[server_id] == credential