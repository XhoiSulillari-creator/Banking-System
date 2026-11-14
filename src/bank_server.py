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
        self.server_authentication_service = (
            server_authentication_service
        )
        self.server_id = server_id

    def start(self):
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
    )

        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
    )

        server_socket.bind((self.host, self.port))
        server_socket.listen()

        print(
            f"{self.bank.name} listening on "
            f"{self.host}:{self.port}"
    )

        while True:
            connection, address = server_socket.accept()

            print(f"Connection received from {address}")

            data = connection.recv(1024)
            message = data.decode()

            print(f"Message received: {message}")

            if message.startswith("LOGIN:"):
                response = self._handle_customer_login(message)

            elif message.startswith("SERVER_LOGIN:"):
                response = self._handle_server_login(message)

            elif message.startswith("TRANSFER_PREPARE:"):
                response = self._handle_transfer_prepare(message)

            elif message.startswith("TRANSFER_COMMIT:"):
                response = self._handle_transfer_commit(message)

            elif message == "GET_BANK_NAME":
                response = self.bank.name

            else:
                response = "Unknown request"

            connection.sendall(response.encode())
            connection.close()
    
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

    def _handle_transfer_prepare(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid transfer request"

        account_id = parts[1]

        try:
            amount = float(parts[2])
        except ValueError:
            return "Invalid transfer amount"

        if amount <= 0:
            return "Invalid transfer amount"

        account = self.bank.get_account(account_id)

        if account is None:
            return "Destination account not found"

        return "Transfer prepared"

    def _handle_transfer_commit(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid transfer request"

        account_id = parts[1]

        try:
            amount = float(parts[2])
        except ValueError:
            return "Invalid transfer amount"

        if self.bank.credit_account(account_id, amount):
            return "Transfer committed"

        return "Transfer commit failed"

    def authenticate_with_server(
        self,
        host,
        port,
        server_id,
        credential
    ):
        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client_socket.connect((host, port))

        message = (
            f"SERVER_LOGIN:"
            f"{self.server_id}:"
            f"{credential}"
        )

        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()

        client_socket.close()

        return response

    def execute_interbank_transfer(
        self,
        remote_host,
        remote_port,
        remote_server_id,
        remote_credential,
        source_account_id,
        destination_account_id,
        amount
    ):
        authentication_response = (
            self.authenticate_with_server(
                remote_host,
                remote_port,
                remote_server_id,
                remote_credential
            )
        )

        if authentication_response != (
            "Server authentication successful"
        ):
            return False

        prepare_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        prepare_socket.connect(
            (remote_host, remote_port)
        )

        prepare_message = (
            f"TRANSFER_PREPARE:"
            f"{destination_account_id}:"
            f"{amount}"
        )

        prepare_socket.sendall(
            prepare_message.encode()
        )

        prepare_response = (
            prepare_socket.recv(1024).decode()
        )

        prepare_socket.close()

        if prepare_response != "Transfer prepared":
            return False

        if not self.bank.debit_account(
            source_account_id,
            amount
        ):
            return False

        commit_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            commit_socket.connect(
                (remote_host, remote_port)
            )

            commit_message = (
                f"TRANSFER_COMMIT:"
                f"{destination_account_id}:"
                f"{amount}"
            )

            commit_socket.sendall(
                commit_message.encode()
            )

            commit_response = (
                commit_socket.recv(1024).decode()
            )

        finally:
            commit_socket.close()

        if commit_response == "Transfer committed":
            return True

        self.bank.credit_account(
            source_account_id,
            amount
        )

        return False