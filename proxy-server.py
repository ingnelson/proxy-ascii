import socket
import os
from _thread import *
import urllib.parse as urlparse
import re
from textwrap import wrap

# Create a TCP/IP socket
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#ServerSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG, 200 ) # Test this option for limit send bytes to the client
#ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000)    # Test this option for limit send bytes to the client
IP = '0.0.0.0'
PORT = 80
ThreadCount = 0
try:
    server_address = (IP , PORT)
    ServerSocket.bind((server_address))
    print('starting up on {} port {}'.format(*server_address))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(100)



def threaded_client(connection):

    while True:
        data = connection.recv(4096)
        request = data.decode('utf-8')
        print('request from client: ', format(data))
        print('received %s bytes from %s' % (len(data), address))
        request = data.decode('utf-8')
        request = request.split('#')[1]
        request = re.sub('#', '', request)
        #print(request)
        password = ''.join(urlparse.parse_qs(request)['0'])
        method = int(''.join(urlparse.parse_qs(request)['method']))
        bytes_request = int(''.join(urlparse.parse_qs(request)['down']))
        print('%s  bytes requested via URL by the client:' % bytes_request)
        if request and password == 'fown' and method == 1:
           response = '0\r\n'
           connection.sendall(response.encode('utf-8'))
           print('sent %s bytes back to %s: ' % (len(response), address))
        elif request and password == 'fown' and method == 2:
           response = bytes_request * 'D' + 'D\r\n'
           connection.send(b'HTTP/1.1 200 Connection established\r\n\r\n')
           connection.sendall(response.encode('utf-8'))
           print('sent %s bytes back to %s: ' % (len(response), address))
        elif request and password == 'fown' and method == 3:
           response = bytes_request * 'D' + 'D'
           connection.send(b'HTTP/1.1 200 0K\r\n\r\n')
           connection.sendall(response.encode('utf-8'))
           print('sent %s bytes back to %s: ' % (len(response), address))
        elif request and password == 'fown' and method == 4:
           response = (os.urandom(998) + b'\r\n')*500
           print('sent %s bytes back to %s: ' % (len(response), address))
           connection.sendall(response)
        elif request and password == 'fown' and method == 5:
           response = bytes_request * 'D' + '\r\n'
           if len(response) > 1000:
                    response = wrap(response,1386)
                    response = [item + '\r\n' for item in response]
                    response = ''.join(response)
                    connection.sendall(response.encode('utf-8'))
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

if __name__=="__main__":
    main()
