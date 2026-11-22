import socket
from bank_logger import get_bank_logger
from session_service import SessionService
from login_command import LoginCommand
from get_account_command import GetAccountCommand

class BankServer:
    def __init__(
            self,
            bank,
            host,
            port,
            server_authentication_service,
            server_id,
            admin_authentication_service,
            peer_credentials,
            session_service

):
            self.bank = bank
            self.host = host
            self.port = port
            self.server_authentication_service = (
            server_authentication_service
        )
            self.server_id = server_id
            self.peer_credentials = peer_credentials
            self.session_service = session_service
            self.admin_authentication_service = (
            admin_authentication_service
        )
            self.logger = get_bank_logger()

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
                command = LoginCommand(
                self,
                message
                )

                response = command.execute()

            elif message.startswith("GET_ACCOUNT:"):
                command = GetAccountCommand(
                    self,
                    message
    )

                response = command.execute()

            elif message.startswith("TRANSFER:"):
                response = self._handle_customer_transfer(message)

            elif message.startswith("REQUEST_OTP:"):
                response = self._handle_request_otp(message)

            elif message.startswith("ADMIN_LOGIN:"):
                response = self._handle_admin_login(message)

            elif message.startswith("ADMIN_ACCOUNT:"):
                response = self._handle_admin_account(message)

            elif message.startswith("ADMIN_STATISTICS:"):
                response = self._handle_admin_statistics(message)

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
            token = self.session_service.create_session(
                customer_id
        )

            print("SESSION CREATED:", token)
            print("SESSIONS:", self.session_service.sessions)

            self.logger.info(
                f"Customer login successful: {customer_id}"
        )

            return f"Login successful|Token:{token}"

        self.logger.warning(
            f"Customer login failed: {customer_id}"
    )

        return "Login failed"

    def _handle_get_account(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid account request"

        token = parts[1]
        account_id = parts[2]

        customer_id = self.session_service.get_identity(token)

        print("SESSION LOOKUP TOKEN:", token)
        print("SESSIONS:", self.session_service.sessions)
        print("CUSTOMER FROM SESSION:", customer_id)

        if customer_id is None:
            self.logger.warning(
                "Account request rejected: invalid session"
        )
            return "Authentication required"

        account = self.bank.get_account(account_id)

        if account is None:
            return "Account not found"

        if account.owner.customer_id != customer_id:
            self.logger.warning(
                f"Unauthorized account access attempt: "
                f"customer={customer_id}, account={account_id}"
        )
            return "Access denied"

        return f"Balance:{account.balance}"

    def _handle_customer_transfer(self, message):
        parts = message.split(":")

        if len(parts) != 8:
            return "Invalid transfer request"

        token = parts[1]
        source_account_id = parts[2]
        destination_host = parts[3]
        destination_port = parts[4]
        destination_server_id = parts[5]
        destination_account_id = parts[6]

        customer_id = self.session_service.get_identity(token)

        if customer_id is None:
            self.logger.warning(
                "Transfer request rejected: invalid session"
        )
            return "Authentication required"

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
            self.peer_credentials[destination_server_id],
            source_account_id,
            destination_account_id,
            amount
    )

        if success:
            self.logger.info(
                f"Inter-bank transfer successful: "
                f"{source_account_id} -> "
                f"{destination_account_id}, "
                f"amount={amount}"
        )
            return "Transfer successful"

        self.logger.error(
            f"Inter-bank transfer failed: "
            f"{source_account_id} -> "
            f"{destination_account_id}, "
            f"amount={amount}"
    )

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
            token = self.session_service.create_session(
                admin_id
        )

            self.logger.info(
                f"Admin login successful: {admin_id}"
        )

            return f"Admin login successful|Token:{token}"

        self.logger.warning(
            f"Admin login failed: {admin_id}"
    )

        return "Admin login failed"
    
    def _handle_admin_account(self, message):
        parts = message.split(":")

        if len(parts) != 3:
            return "Invalid admin account request"

        token = parts[1]
        account_id = parts[2]

        admin_id = self.session_service.get_identity(token)

        if admin_id is None:
            self.logger.warning(
                "Admin account request rejected: invalid session"
        )
            return "Authentication required"

        account = self.bank.get_account(account_id)

        if account is None:
            return "Account not found"

        self.logger.info(
            f"Admin account access: admin={admin_id}, "
            f"account={account_id}"
    )

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
            token = self.session_service.create_session(
                server_id
        )

            self.logger.info(
                f"Server login successful: {server_id}"
        )

            return f"Server authentication successful|Token:{token}"

        self.logger.warning(
            f"Server login failed: {server_id}"
    )

        return "Server authentication failed"
    
    def _handle_transfer_prepare(self, message):
        parts = message.split(":")

        if len(parts) != 4:
            return "Invalid transfer request"

        token = parts[1]
        account_id = parts[2]

        try:
            amount = float(parts[3])
        except ValueError:
            return "Invalid transfer amount"

        server_id = self.session_service.get_identity(token)

        if server_id is None:
            self.logger.warning(
                "Transfer prepare rejected: invalid server session"
        )
            return "Authentication required"

        if amount <= 0:
            return "Invalid transfer amount"

        account = self.bank.get_account(account_id)

        if account is None:
            return "Destination account not found"

        self.logger.info(
            f"Transfer prepare authorized: "
            f"server={server_id}, account={account_id}"
    )

        return "Transfer prepared"

    def _handle_transfer_commit(self, message):
        parts = message.split(":")

        if len(parts) != 4:
            return "Invalid transfer request"

        token = parts[1]
        account_id = parts[2]

        try:
            amount = float(parts[3])
        except ValueError:
            return "Invalid transfer amount"

        server_id = self.session_service.get_identity(token)

        if server_id is None:
            self.logger.warning(
                "Transfer commit rejected: invalid server session"
        )
            return "Authentication required"

        if self.bank.credit_account(
            account_id,
            amount
    ):
            self.logger.info(
                f"Transfer commit authorized: "
                f"server={server_id}, account={account_id}"
        )
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
        client_socket.settimeout(5)

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
        try:
            authentication_response = (
                self.authenticate_with_server(
                    remote_host,
                    remote_port,
                    remote_server_id,
                    remote_credential
        )
    )
        except (socket.timeout, ConnectionRefusedError):
            self.logger.error(
                f"Remote bank unavailable: "
                f"{remote_host}:{remote_port}"
            )
            return False

        if not authentication_response.startswith(
            "Server authentication successful|Token:"
        ):
            return False

        server_token = authentication_response.split(
            "Token:",
            1
        )[1]

        prepare_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        prepare_socket.settimeout(5)

        prepare_socket.connect(
            (remote_host, remote_port)
        )

        prepare_message = (
            f"TRANSFER_PREPARE:"
            f"{server_token}:"
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
        commit_socket.settimeout(5)

        try:
            commit_socket.connect(
                (remote_host, remote_port)
            )

            commit_message = (
                f"TRANSFER_COMMIT:"
                f"{server_token}:"
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

    def _handle_admin_statistics(self, message):
        parts = message.split(":")

        if len(parts) != 2:
            return "Invalid admin statistics request"

        token = parts[1]

        admin_id = self.session_service.get_identity(token)

        if admin_id is None:
            self.logger.warning(
                "Admin statistics request rejected: invalid session"
        )
            return "Authentication required"

        statistics = self.bank.get_statistics()

        self.logger.info(
            f"Admin statistics accessed: admin={admin_id}"
    )

        return (
            f"Customers:{statistics['customers']}"
            f"|Accounts:{statistics['accounts']}"
            f"|TotalBalance:{statistics['total_balance']}"
    )