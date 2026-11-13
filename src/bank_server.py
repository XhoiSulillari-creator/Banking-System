import socket


class BankServer:
    def __init__(
        self,
        bank,
        host,
        port,
        server_authentication_service,
        server_id
    ):
        self.bank = bank
        self.host = host
        self.port = port
        self.server_authentication_service = server_authentication_service
        self.server_id = server_id

    def start(self):
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server_socket.bind((self.host, self.port))
        server_socket.listen()

        print(
            f"{self.bank.name} listening on "
            f"{self.host}:{self.port}"
        )

        connection, address = server_socket.accept()

        print(f"Connection received from {address}")

        data = connection.recv(1024)
        message = data.decode()

        print(f"Message received: {message}")

        if message.startswith("LOGIN:"):
            response = self._handle_customer_login(message)

        elif message.startswith("SERVER_LOGIN:"):
            response = self._handle_server_login(message)

        elif message == "GET_BANK_NAME":
            response = self.bank.name

        else:
            response = "Unknown request"

        connection.sendall(response.encode())

        connection.close()
        server_socket.close()

    def _handle_customer_login(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid login request"

        customer_id = parts[1]
        password = parts[2]

        if self.bank.authenticate_customer(
            customer_id,
            password
        ):
            return "Login successful"

        return "Login failed"

    def _handle_server_login(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid server login request"

        server_id = parts[1]
        credential = parts[2]

        if self.server_authentication_service.authenticate(
            server_id,
            credential
        ):
            return "Server authentication successful"

        return "Server authentication failed"

    def authenticate_with_server(self, host, port, server_id, credential):
        client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

        client_socket.connect((host, port))

        message = f"SERVER_LOGIN:{self.server_id}:{credential}"

        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()

        client_socket.close()

        return response