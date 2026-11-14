import socket


class CustomerClient:
    def __init__(
        self,
        host,
        port
    ):
        self.host = host
        self.port = port
        self.customer_id = None
        self.password = None

    def send_request(self, message):
        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client_socket.connect(
            (self.host, self.port)
        )

        client_socket.sendall(
            message.encode()
        )

        response = client_socket.recv(
            1024
        ).decode()

        client_socket.close()

        return response

    def login(self, customer_id, password):
        response = self.send_request(
            f"LOGIN:{customer_id}:{password}"
        )

        if response == "Login successful":
            self.customer_id = customer_id
            self.password = password

        return response

    def get_account_balance(self, account_id):
        return self.send_request(
            f"GET_ACCOUNT:"
            f"{self.customer_id}:"
            f"{account_id}"
        )

    def transfer(
        self,
        source_account_id,
        destination_host,
        destination_port,
        destination_server_id,
        destination_account_id,
        amount
    ):
        return self.send_request(
            f"TRANSFER:"
            f"{self.customer_id}:"
            f"{source_account_id}:"
            f"{destination_host}:"
            f"{destination_port}:"
            f"{destination_server_id}:"
            f"{destination_account_id}:"
            f"{amount}"
        )