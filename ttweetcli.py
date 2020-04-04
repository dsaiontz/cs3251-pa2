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
        
    while True:
        response = s.recv(512).decode()
        if response.equals('Goodbye!'):
            print(response)
            return
        while not response.equals('Ready'):
            response = s.recv(512).decode()
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

    #old, unaltered code begins here

    #NOTE: PORTIONS OF THIS SECTION CAN BE USED FOR TWEET OPERATION
    if(len(message) <= 150):
        #receive current message if any is available
        if setting == '-d':
            #send to server that client wishes to download current saved message
            s.sendall('download'.encode())
            #receive saved message
            data = s.recv(256).decode() #make sure enough space for 150 character message
            #check that message received is not that there is no message
            if data != 'no message stored':
                print('output: \"' + data + '\"')
            else:
                print('output: \"\"')
    
        elif setting == '-u':
            #send to server that client wishes to upload a new message
            s.sendall('upload'.encode())
            data = s.recv(256).decode()
            #verify that server is ready to receive the message
            if data == 'ready':
                #send the message to server
                s.sendall(message.encode())
                #check that server saved the message successfully
                data = s.recv(256).decode()
                if data == 'ok':
                    print('upload successful')
                else:
                    print('ERROR message unable to be saved: ' + data)
            #if the server for some reason was unable to process an upload request
            else:
                print('ERROR message not able to be sent to server')
        #if any other command in terminal, notify user that arg not valid
        else:
            print('ERROR Command not valid, use either -u or -d')
    #message is greater than 150 characters, return an error
    else:
        print('ERROR message length > 150')

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