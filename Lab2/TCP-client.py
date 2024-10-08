import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1745))

message = "Какое-то сообщение для сервера"
client_socket.sendall(message.encode())
data = client_socket.recv(1024)
print(f"Ответ от сервера: {data.decode()}")

client_socket.close()