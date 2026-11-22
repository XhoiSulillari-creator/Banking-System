import socket


class AdminClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.admin_id = None
        self.session_token = None

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

    def request_otp(self, admin_id):
        return self.send_request(
            f"REQUEST_OTP:{admin_id}"
        )

    def login(self, admin_id, otp):
        response = self.send_request(
            f"ADMIN_LOGIN:{admin_id}:{otp}"
        )

        if response.startswith(
            "Admin login successful|Token:"
        ):
            self.admin_id = admin_id
            self.session_token = response.split(
                "Token:",
                1
            )[1]

        return response

    def get_account(self, account_id):
        if self.session_token is None:
            return "Admin authentication required"

        return self.send_request(
            f"ADMIN_ACCOUNT:"
            f"{self.session_token}:"
            f"{account_id}"
        )

    def get_statistics(self):
        if self.session_token is None:
            return "Admin authentication required"

        return self.send_request(
            f"ADMIN_STATISTICS:"
            f"{self.session_token}"
        )