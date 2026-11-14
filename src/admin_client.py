import socket


class AdminClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.admin_id = None
        self.authenticated = False

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

        if response == "Admin login successful":
            self.admin_id = admin_id
            self.authenticated = True

        return response

    def get_account(self, account_id):
        if not self.authenticated:
            return "Admin authentication required"

        return self.send_request(
            f"ADMIN_ACCOUNT:{account_id}"
    )

    def get_statistics(self):
        if not self.authenticated:
            return "Admin authentication required"

        return self.send_request(
            "ADMIN_STATISTICS"
    )