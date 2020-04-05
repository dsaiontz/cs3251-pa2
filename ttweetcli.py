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
    port = str(sys.argv[2])

    #Define the port on which you want to connect 
    if port < 0 or port > 65535:
        print('error: server port invalid, connection refused.')
        return

    username = sys.argv[4]
    if not username.isalnum():
        print('error: username has wrong format, connection refused.')
        return
    
    #create a socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    #attempt to connect to server before checking if length of message is <= 150 characters
    try:
        s.connect((host, port))
    except:
        print('error: server not found.')
        return
    
    s.sendall(('username = ' + username).encode())
    data = s.recv(512).decode()
    if data.equals('username illegal, connection refused.'):
        print(data)
        return
    
    if data.equals(''):
        print('error: server unable to be reached')
        return

    if data.equals('username legal, connection established.'):
        print(data)
    else:
        print('error: unknown error')
        return

    timeline = []
        
    while True:
        response = s.recvall(512).decode()
        print(response)
        if response.equals('bye bye'):
            return
        while not response.equals('Ready for next input'):
            if not response.equals('bye bye') or not response.equals('message length illegal, connection refused.') or not response.equals('hashtag illegal format, connection refused.') or not response.equals('error: username has wrong format, connection refused.'):
                timeline.insert(0, response)
            response = s.recvall(512).decode()
            print(response)
        command = input('User command: ')

        if len(command) > 5 and command[0, 5].equals('tweet'):
            if len(command) < 7:
                print('message length illegal, connection refused.')
                continue
            messageAndHashTag = command[7:]
            if messageAndHashTag.find('"') == messageAndHashTag.rfind('"'):
                print('hashtag illegal format, connection refused.')
                continue
            message = messageAndHashTag[0:messageAndHashTag.find('"')]
            if len(message) > 150 or len(message) < 0:
                print('message length illegal, connection refused.')
                continue
            hashTags = messageAndHashTag[:messageAndHashTag.find('"') + 2]
            if len(hashTags) == 0 or hashTags.find('##') > -1 or hashTags.count('#') > 5 or hashTags.find('#ALL') > -1:
                print('hashtag illegal format, connection refused.')
                continue
            lastIndex = 0
            curHashTagsLeft = hashTags
            shouldExitCommand = False
            while lastIndex != hashTags.rfind('#'):
                if curHashTagsLeft[1:].find('#') > 15:
                    print('hashtag illegal format, connection refused.')
                    shouldExitCommand = True
                    break
                else:
                    curHashTagsLeft = curHashTagsLeft[curHashTagsLeft[1:].find('#'):]
            if shouldExitCommand:
                continue
            if len(curHashTagsLeft) > 15:
                print('hashtag illegal format, connection refused.')
                continue
            s.sendall(command.encode())
        
        if len(command) > 9 and command[0, 9].equals('subscribe'):
            if len(command) < 11:
                print('hashtag illegal format, connection refused.')
                continue
            hashTag = command[11:]
            if len(hashTag) == 0 or not hashTag[0].equals('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                print('hashtag illegal format, connection refused.')
                continue
            if len(hashTag) > 15:
                print('hashtag illegal format, connection refused.')
                continue
            s.sendall(command.encode())

        if len(command) > 11 and command[0, 11].equals('unsubscribe'):
            if len(command) < 13:
                print('hashtag illegal format, connection refused.')
                continue
            hashTag = command[13:]
            if len(hashTag) == 0 or not hashTag[0].equals('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                print('hashtag illegal format, connection refused.')
                continue
            if len(hashTag) > 15:
                print('hashtag illegal format, connection refused.')
                continue
            s.sendall(command.encode())

        if command.equals('timeline'):
            for tweet in timeline:
                print(tweet)
            s.sendall(command.encode())
        
        if command.equals('getusers'):
            s.sendall(command.encode())

        if len(command) > 9 and command[0:9].equals('gettweets'):
            if len(command < 11):
                print('error: username has wrong format, connection refused.')
                continue
            if not command[11:].isalnum():
                print('error: username has wrong format, connection refused.')
                continue
            s.sendall(command.encode())

        if command.equals('exit'):
            s.sendall(command)

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