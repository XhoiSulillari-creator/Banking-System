import socket


client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect(
    ("127.0.0.1", 5002)
)

message = "SERVER_LOGIN:BANK_ALBANIA:wrong-credential"

client_socket.sendall(message.encode())

response = client_socket.recv(1024).decode()

print(f"Server response: {response}")

client_socket.close()