#import socket module
import socket
import sys
import re

def Main():

    if len(sys.argv) != 4:
        print('error: args should contain <ServerIP> <ServerPort> <Username>')
        return

    #host for socket
    host = sys.argv[1]
    ipParts = host.split('.')
    if len(ipParts) != 4:
        print('error: server ip invalid, connection refused.')
        return
    for x in ipParts:
        if not x.isdecimal():
            print('error: server ip invalid, connection refused.')
            return
        y = int(x)
        if y < 0 or y > 255:
            print('error: server ip invalid, connection refused.')
            return

    #port for socket
    port = int(sys.argv[2]) ######changed str to int

    #Define the port on which you want to connect
    if port < 1024 or port > 65535:
        print('error: server port invalid, connection refused.')
        return

    username = sys.argv[3]
    if not username.isalnum():
        print('error: username has wrong format, connection refused.')
        return

    #create a socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #attempt to connect to server before checking if length of message is <= 150 characters
    try:
        s.connect((host, port)) #ip, port
    except:
        print('error: server not found.')   ########is this correct????
        return

    s.sendall((username).encode())
    data = s.recv(512).decode()
    if data == ('username illegal, connection refused.'):
        print(data)
        return

    if data == (''):
        print('error: server unable to be reached')
        return

    if data == ('username legal, connection established.'):
        print(data)
    else:
        print('error: unknown error')
        return

    timeline = []

    getTweetsWasUsed = False
    getUsersWasUsed = False
    subscribeWasUsed = False
    timelineWasUsed = False

    while True:
        response = s.recv(512).decode()  #response is entire thing?
        if response != 'Ready for next input':
            print(response)
        if response == ('bye bye'):
            return
        if response != ('Ready for next input'): ###while
            if not getTweetsWasUsed and not getUsersWasUsed and not subscribeWasUsed and (not response == ('bye bye') or not response == ('message length illegal, connection refused.') or not response == ('hashtag illegal format, connection refused.') or not response == ('error: username has wrong format, connection refused.')):
                timeline.append(response)
            #response = s.recv(512).decode()
            #print(response)
            s.sendall("continue".encode())
            continue
        getTweetsWasUsed = False
        getUsersWasUsed = False
        subscribeWasUsed = False
        timelineWasUsed = False
        #print("test") #NOT GETTING HERE
        command = input('')

        if len(command) > 5 and command[0: 5] == ('tweet'):
            if len(command) < 7:
                print('message length illegal, connection refused.')
                s.sendall('timeline'.encode())
                continue
            messageAndHashTag = command[6:]
            if messageAndHashTag.find('"') == messageAndHashTag.rfind('"'):
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            message = messageAndHashTag[0:messageAndHashTag.rfind('"')]
            if len(message) > 150 or len(message) < 0:
                print('message length illegal, connection refused.')
                s.sendall('timeline'.encode())
                continue
            hashTags = messageAndHashTag[:messageAndHashTag.rfind('"') + 2]
            if len(hashTags) == 0 or hashTags.find('##') > -1 or hashTags.count('#') > 5 or hashTags.find('#ALL') > -1:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            allHashTags = hashTags.split('#')
            shouldExitCommand = False
            for hashTag in allHashTags:
                if len(hashTag) > 14:
                    print('hashtag illegal format, connection refused.')
                    shouldExitCommand = True
                    break
            if shouldExitCommand:
                s.sendall('timeline'.encode())
                continue
            s.sendall(command.encode())

        if len(command) > 9 and command[0: 9] == ('subscribe'):
            if len(command) < 11:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            hashTag = command[10:]
            print(hashTag)
            if len(hashTag) == 0 or not hashTag[0] == ('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            if len(hashTag) > 15:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            subscribeWasUsed = True
            s.sendall(command.encode())

        if len(command) > 11 and command[0: 11] == ('unsubscribe'):
            if len(command) < 12:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            hashTag = command[12:]
            if len(hashTag) == 0 or not hashTag[0] == ('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            if len(hashTag) > 15:
                print('hashtag illegal format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            s.sendall(command.encode())

        if command == ('timeline'):
            for tweet in timeline:
                print(tweet)
            timelineWasUsed = True
            s.sendall(command.encode())

        if command == ('getusers'):
            getUsersWasUsed = True
            s.sendall(command.encode())

            responseUsers = ''
            while True:
                responseUsers = s.recv(512).decode()
                if responseUsers == 'finished':
                    s.sendall('received'.encode())
                    break
                print(responseUsers)
                s.sendall('continue'.encode())
            continue




        if len(command) > 9 and command[0:9] == ('gettweets'):
            if len(command) < 10:
                print('error: username has wrong format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            if not command[10:].isalnum():
                print('error: username has wrong format, connection refused.')
                s.sendall('timeline'.encode())
                continue
            getTweetsWasUsed = True
            s.sendall(command.encode())

        if command == ('exit'):
            s.sendall(command.encode())

if __name__ == '__main__':
    Main()

#based on following code from https://pymotw.com/3/socket/tcp.html
# import socket
# import sys

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('localhost', 10000)
# print('connecting to {} port {}'.format(*server_address))
# sock.connect(server_address)

# try:

#     # Send data
#     message = b'This is the message.  It will be repeated.'
#     print('sending {!r}'.format(message))
#     sock.sendall(message)

#     # Look for the response
#     amount_received = 0
#     amount_expected = len(message)

#     while amount_received < amount_expected:
#         data = sock.recv(16)
#         amount_received += len(data)
#         print('received {!r}'.format(data))

# finally:
#     print('closing socket')
#     sock.close()

#also based on following code found at https://realpython.com/python-sockets/#echo-client
# import socket

# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))