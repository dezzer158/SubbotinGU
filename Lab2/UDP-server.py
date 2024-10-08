import socket

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(('localhost', 12345))
print("Сервер ожидает сообщений")

while True:
    data, addr = udp_server_socket.recvfrom(1024)
    print(f"Сообщение от {addr}: {data.decode()}")
    udp_server_socket.sendto(data, addr)
