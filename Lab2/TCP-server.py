import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1745))

server_socket.listen(1)
print("Сервер ожидает подключения...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент с адресом {addr}")
    data = client_socket.recv(1024)
    if not data:
        break
    print(f"Сообщение от клиента: {data.decode()}")
    client_socket.sendall(data)
    client_socket.close()