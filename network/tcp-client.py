import socket

target_host = "localhost"
target_port = 8088

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port));

client.send(b"GET / HTTP/1.1\r\nHost: www.163.com\r\n\r\n");

response = client.recv(4096)

print(response.decode())

client.close()
