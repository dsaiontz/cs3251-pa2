import socket

from _thread import *
import sys

#current message

def Main():
   host = ""
   message = ''

   #port number for server
   serverPort = int(sys.argv[1])

   #create socket and bind it with host and port
   serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   serverSocket.bind(('127.0.0.1', port))

   #put the socket into listening mode
   s.listen(1)

   #a forever loop until client wants to exit
   while True:

      #establish connection with client
      conn, addr = s.accept()
      #start a new thread and determine if client wants to upload or download
      data = conn.recv(256).decode()
      if data == 'download':
         #check that message is instantiated (defensive coding, make sure there is a valid string)
         if message != None:
            conn.sendall(message.encode())
         else:
         #otherwise, send an empty message
            conn.sendall(''.encode())
      elif data == 'upload':
         #send to client that server is ready to receive new message
         conn.sendall('ready'.encode())
         data = conn.recv(256).decode()
         #check message for length
         if len(data) > 150:
            conn.sendall('message >150 characters'.encode())
         message = data
         #send to client that message was successfully saved
         conn.sendall('ok'.encode())
      #close connection to client regardless
      conn.close()
   s.close()


if __name__ == '__main__':
   Main()

#based on following code from https://pymotw.com/3/socket/tcp.html
# import socket
# import sys

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print('starting up on {} port {}'.format(*server_address))
# sock.bind(server_address)

# # Listen for incoming connections
# sock.listen(1)

# while True:
#     # Wait for a connection
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#     try:
#         print('connection from', client_address)

#         # Receive the data in small chunks and retransmit it
#         while True:
#             data = connection.recv(16)
#             print('received {!r}'.format(data))
#             if data:
#                 print('sending data back to the client')
#                 connection.sendall(data)
#             else:
#                 print('no data from', client_address)
#                 break

#     finally:
#         # Clean up the connection
#         connection.close()

#also based on following code found at https://realpython.com/python-sockets/#echo-server
# import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)