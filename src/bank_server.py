import socket


class BankServer:
    def __init__(
        self,
        bank,
        host,
        port,
        server_authentication_service,
        server_id,
        admin_authentication_service
    ):
        self.bank = bank
        self.host = host
        self.port = port
        self.server_authentication_service = (
            server_authentication_service
        )
        self.server_id = server_id
        self.admin_authentication_service = (
            admin_authentication_service
        )

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

            elif message.startswith("GET_ACCOUNT:"):
                response = self._handle_get_account(message)

            elif message.startswith("TRANSFER:"):
                response = self._handle_customer_transfer(message)

            elif message.startswith("REQUEST_OTP:"):
                response = self._handle_request_otp(message)

            elif message.startswith("ADMIN_LOGIN:"):
                response = self._handle_admin_login(message)

            elif message.startswith("ADMIN_ACCOUNT:"):
                response = self._handle_admin_account(message)

            elif message == "ADMIN_STATISTICS":
                response = self._handle_admin_statistics()

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

    def _handle_get_account(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid account request"

        customer_id = parts[1]
        account_id = parts[2]

        customer = self.bank.get_customer(customer_id)

        if customer is None:
            return "Customer not found"

        account = self.bank.get_account(account_id)

        if account is None:
            return "Account not found"

        if account.owner.customer_id != customer_id:
            return (
                "Access denied: account does not "
                "belong to customer"
            )

        return f"Balance:{account.balance}"

    def _handle_customer_transfer(self, message):
        parts = message.split(":")

        if len(parts) != 8:
            return "Invalid transfer request"

        customer_id = parts[1]
        source_account_id = parts[2]
        destination_host = parts[3]
        destination_port = parts[4]
        destination_server_id = parts[5]
        destination_account_id = parts[6]

        try:
            amount = float(parts[7])
            destination_port = int(destination_port)
        except ValueError:
            return "Invalid transfer amount or port"

        source_account = self.bank.get_account(
            source_account_id
        )

        if source_account is None:
            return "Source account not found"

        if source_account.owner.customer_id != customer_id:
            return (
                "Access denied: source account does not "
                "belong to customer"
            )

        if amount <= 0:
            return "Transfer amount must be greater than zero"

        success = self.execute_interbank_transfer(
            destination_host,
            destination_port,
            destination_server_id,
            "alb-server-123",
            source_account_id,
            destination_account_id,
            amount
        )

        if success:
            return "Transfer successful"

        return "Transfer failed"

    def _handle_request_otp(self, message):
        parts = message.split(":")

        if len(parts) != 2:
            return "Invalid OTP request"

        admin_id = parts[1]

        return self.admin_authentication_service.request_otp(
            admin_id
        )

    def _handle_admin_login(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid admin login request"

        admin_id = parts[1]
        otp = parts[2]

        if self.admin_authentication_service.authenticate(
            admin_id,
            otp
        ):
            return "Admin login successful"

        return "Admin login failed"

    def _handle_admin_account(self, message):
        parts = message.split(":")

        if len(parts) != 2:
            return "Invalid admin account request"

        account_id = parts[1]

        account = self.bank.get_account(account_id)

        if account is None:
            return "Account not found"

        return (
            f"Account:{account.account_id}"
            f"|Customer:{account.owner.customer_id}"
            f"|Balance:{account.balance}"
        )

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

        if self.bank.credit_account(
            account_id,
            amount
        ):
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

        client_socket.connect(
            (host, port)
        )

        message = (
            f"SERVER_LOGIN:"
            f"{self.server_id}:"
            f"{credential}"
        )

        client_socket.sendall(message.encode())

        response = client_socket.recv(
            1024
        ).decode()

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

        prepare_response = prepare_socket.recv(
            1024
        ).decode()

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

            commit_response = commit_socket.recv(
                1024
            ).decode()

        finally:
            commit_socket.close()

        if commit_response == "Transfer committed":
            return True

        self.bank.credit_account(
            source_account_id,
            amount
        )

        return False

    def _handle_admin_statistics(self):
        statistics = self.bank.get_statistics()

        return (
            f"Customers:{statistics['customers']}"
            f"|Accounts:{statistics['accounts']}"
            f"|TotalBalance:{statistics['total_balance']}"
    )