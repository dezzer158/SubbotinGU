import socket

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Сообщение для сервера"
udp_client_socket.sendto(message.encode(), ('localhost', 12345))
data, addr = udp_client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

udp_client_socket.close()
