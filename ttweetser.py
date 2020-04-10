import socket

from _thread import *
import threading
import sys

#current message

#key: username, value: ([tweets sent], connectionSocket, addr)
users = {}
#key: hashtag, value: [usernames]
hashtags = {}



#port number for server
port = int(sys.argv[1])

#create socket and bind it with host and port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))

#put the socket into listening mode
print('The server is ready to receive')
s.listen(5)

def threaded_client(connection, user):
   global hashtags
   global users
   numSubbed = 0
   while True:
      connection.send('020Ready for next input'.encode())
      #receive message from client
      try:
         receivedLength = int(connection.recv(3).decode())
         received = str(connection.recv(receivedLength).decode())
      except Exception:
         connection.send('020error: cause unknown'.encode())
      print('Command: ' + received)


      #Tweet command
      if received[0:5] == "tweet":   #tweet
         print('got tweet')
         #supposed to get tweet between quotations
         tweetContent = received[received.find('"'):]
         afterMessage = received[received.rfind('"'):]
         hashtagFull = afterMessage[afterMessage.find('#'):]
         hashtagList = []
         currentHashtag = ''
         i = 0
         for char in hashtagFull:
            if char == '#':
               if i == 0:
                  currentHashtag = currentHashtag + char
               else:
                  hashtagList.append(currentHashtag)
                  currentHashtag = '#'
               i = i + 1
            else:
               currentHashtag = currentHashtag + char
               if (i == len(hashtagFull) - 1):
                  hashtagList.append(currentHashtag)
               else:
                  i = i + 1
         print(str(hashtagList))
         #process tweet
         tweetContent = user + ' ' + tweetContent
         users[user][0].append(tweetContent)
         lengthOfContent = str(len(tweetContent))
         lengthOfContent = lengthOfContent.zfill(3)
         tweetContent = lengthOfContent + tweetContent
         hashtagList.append('#ALL')
         #send tweet to clients subscribed to each mentioned hashtag
         usersSentTo = []
         for tag in hashtagList:
            if tag in hashtags:
               for userPerson in hashtags[tag]:
                  if userPerson not in usersSentTo:
                     connectionS = users[userPerson][1] #connection of that user
                     connectionS.send(tweetContent.encode())
                     connectionS.send('020Ready for next input'.encode())
                     usersSentTo.append(userPerson)
         connection.send('020Ready for next input'.encode())





      #subscribe command
      elif received[0:9] == 'subscribe':
         tag = received[10:]
         print(tag)
         count = 0
         if numSubbed == 3:
            toSend = 'operation failed: sub ' + tag + ' failed, already exists or exceeds 3 limitation'
            toSendLen = str(len(toSend))
            toSendLen.zfill(3)
            connection.send((toSendLen + toSend).encode())
            connection.send('020Ready for next input'.encode())
            continue
         if tag in hashtags.keys():
            hashtags[tag].append(user)
         else:
            hashtags[tag] = []
            hashtags[tag].append(user)
         connection.send('017operation success'.encode())
         connection.send('020Ready for next input'.encode())
         numSubbed = numSubbed + 1



      #unsubscribe command
      elif received[0:11] == 'unsubscribe':
         tag = received[12:]
         if tag == '#ALL':
            for htag in hashtags.keys():
               if user in hashtags[htag]:
                  hashtags[htag].remove(user)
         else:
            if tag in hashtags.keys():
               hashtags[tag].remove(user)
         connection.send('017operation success'.encode())
         connection.send('020Ready for next input'.encode())



      #timeline command
      elif received == 'timeline':
         connection.send('020Ready for next input'.encode())

      elif received == 'error':
         connection.send('020Ready for next input'.encode())


      #getusers command
      elif received == 'getusers':
         userList = []
         for user in users.keys():
            lengthOfUser = str(len(user))
            lengthOfUser = lengthOfUser.zfill(3)
            connection.send((lengthOfUser + user).encode())
         connection.send('008finished'.encode())
         connection.send('020Ready for next input'.encode())


      #gettweets command
      elif received[0:9] == 'gettweets':
         uName = received[10:]
         for ttweet in users[uName][0]:
            ttweet = ttweet[0:len(uName)] + ':' + ttweet[len(uName):]
            lengthOfTweet = str(len(ttweet))
            lengthOfTweet = lengthOfTweet.zfill(3)
            connection.send((lengthOfTweet + ttweet).encode())

         connection.send('020Ready for next input'.encode())

      elif received[0:4] == 'exit':
         userExitting = received[5:]
         for hashtag in hashtags.keys():
            if userExitting in hashtags[hashtag]:
               hashtags[hashtag].remove(userExitting)
         del users[userExitting]
         connection.send('007bye bye'.encode())
         connection.close()
         return




#a forever loop until client wants to exit
while True:
   #establish connection with client
   #addr is address bound to socket on other end of connection
   #connectionSocket is new socket object usable to send and receive data
   connectionSocket, addr = s.accept()

   #start a new thread and determine if client wants to upload or download
   try:
      dataLength = int(connectionSocket.recv(3).decode())
      data = connectionSocket.recv(dataLength).decode()
   except Exception:
      connectionSocket.send('037username illegal, connection refused.'.encode())

   #if user exists
   if data in users:
      connectionSocket.send('037username illegal, connection refused.'.encode())
   else:
      connectionSocket.send('039username legal, connection established.'.encode())
      users[data] = ([], connectionSocket, addr, {})

      ip, port = str(addr[0]), str(addr[1])
      print("connected with " + ip + ":" + port + ', ' + data)

      start_new_thread(threaded_client, (connectionSocket, data)) ###may not be able to have data here

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