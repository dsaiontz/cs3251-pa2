import socket

from _thread import *
import threading
import sys

#current message

lock = threading.Lock()

#key: username, value: ([hashtags], [tweets], connectionSocket, addr)
users = {}
#key: hashtag, value: [usernames]
hashtags = {}


#port number for server
serverPort = int(sys.argv[1])

#create socket and bind it with host and port
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', port))

#put the socket into listening mode
print('The server is ready to receive')
s.listen(5)

def threaded_client(connection):
   while True:
      #receive message from client
      received = connection.recv(512).decode()


      #Tweet command
      if received[0:5] == "Tweet":   #tweet
         #supposed to get tweet between quotations
         tweetContent = received[received.find('"') + 1: received.find('"')]
         hashtagFull = received[received.find('#'):]
         hashtags = []
         currentHashtag = ''
         i = 0
         for char in hashtagFull:
            if char == '#':
               if len(hashtags) == 0:
                  currentHashtag = currentHashtag + char
               else:
                  hashtags.append(currentHashtag)
                  currentHashtag = '#'
               i = i + 1
            else:
               currentHashtag = currentHashtag + char
               if (i == len(hashtagFull) - 1):
                  hashtags.append(currentHashtag)
               else:
                  i = i + 1
         #process tweet
         users[]






   connection.close()




#a forever loop until client wants to exit
while True:

   #establish connection with client
   #addr is address bound to socket on other end of connection
   #connectionSocket is new socket object usable to send and receive data
   connectionSocket, addr = s.accept()

   #start a new thread and determine if client wants to upload or download
   data = connectionSocket.recv(256).decode()

   #if user exists
   if data in users:
      connectionSocket.sendall('username illegal, connection refused.'.encode())
   else:
      connectionSocket.sendall('username legal, connection established.'.encode())
      users[data] = ([], [], connectionSocket, addr)

      ip, port = str(addr[0]), str(addr[1])
      print("connected with " + ip + ":" + port)

      start_new_thread(threaded_client, (connectionSocket, ))

s.close()


#if __name__ == '__main__':
#   Main()

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