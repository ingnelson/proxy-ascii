import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.245.22.211', 80)
client_socket.connect(server_address)

request_header = 'GET #0=fown&method=1&down=10# HTTP/1.1\r\n ٌُُُُُُّّّّْْْْْْْْْْْْْْْْْْ\r\n\r\n
client_socket.send(request_header.encode('utf-8'))

response = ''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv

print (response)
client_socket.close()
