import socket


class BankServer:
    def __init__(self, bank, host, port):
        self.bank = bank
        self.host = host
        self.port = port

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
            parts = message.split(":")

            customer_id = parts[1]
            password = parts[2]

            if self.bank.authenticate_customer(
                customer_id,
                password
            ):
                response = "Login successful"
            else:
                response = "Login failed"

        elif message == "GET_BANK_NAME":
            response = self.bank.name

        else:
            response = "Unknown request"

        connection.sendall(response.encode())

        connection.close()
        server_socket.close()