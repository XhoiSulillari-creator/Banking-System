import socket


client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect(
    ("127.0.0.1", 5002)
)

client_socket.sendall(
    b"LOGIN:C006:alice123"
)

print("Message sent")

response = client_socket.recv(1024)

print(f"Server response: {response.decode()}")

client_socket.close()