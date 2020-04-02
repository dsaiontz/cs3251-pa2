#import socket module 
import socket 
import sys
import re
  
def Main(): 

    #setting for client, either upload or download
    setting = sys.argv[1]

    #host for socket
    host = str(sys.argv[2])

    #Define the port on which you want to connect 
    port = int(sys.argv[3])
    if port < 0 or port > 65535:
        print('ERROR port invalid, must be between 0 and 65535')
        return

    message = ''

    if setting == '-u':
        #message provided by client
        message = sys.argv[4]
        #how to escape $'s found at https://stackoverflow.com/questions/18935754/how-to-escape-special-characters-of-a-string-with-single-backslashes
        message = message.translate(str.maketrans({"$":  r"\$", "#": r"\#"}))
    
    #create a socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    #attempt to connect to server before checking if length of message is <= 150 characters
    try:
        s.connect((host, port))
    except:
        print('ERROR Server Not Found')
        return

    #if in download mode, message will always be length 0.
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