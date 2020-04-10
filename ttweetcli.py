#import socket module
import socket
import sys
import re
import threading
import time

#input client thread: receiving commands
#
timeline = []

getTweetsWasUsed = False
getUsersWasUsed = False
subscribeWasUsed = False
timelineWasUsed = False


def Main():

    #timeline = []

    #getTweetsWasUsed = False
    #getUsersWasUsed = False
    #subscribeWasUsed = False
    #timelineWasUsed = False

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
    if not username.isalnum() or username == '':
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

    usernameLen = str(len(username))
    usernameLen = usernameLen.zfill(3)
    s.sendall((str(usernameLen) + username).encode())
    dataLength = int(s.recv(3).decode())
    data = s.recv(dataLength).decode()
    if data == ('username illegal, connection refused.'):
        print(data)
        return

    if data == ('') or data is None:
        print('error: server unable to be reached')
        return

    if data == ('username legal, connection established.'):
        print(data)
    else:
        print('error: ' + data)
        return



    #thread to receive messages from the server
    def clientReceiveThread():
        global timeline
        global getTweetsWasUsed
        global getUsersWasUsed
        global subscribeWasUsed
        global timelineWasUsed

        while True:
            if getUsersWasUsed: #check if getusers was used, it stays in a loop of receiving users until it receives the finished message, at which point it returns to usual activity
                responseLength = int(s.recv(3).decode())
                response = s.recv(responseLength).decode()
                while response != 'finished':
                    print(response)
                    responseLength = int(s.recv(3).decode())
                    response = s.recv(responseLength).decode()
            if getUsersWasUsed:
                getUsersWasUsed = False
                continue
            responseLength = int(s.recv(3).decode())  #we receive 3 bytes first for each message, which represents the length of the message being received
            response = s.recv(responseLength).decode() #we retrieve one message at a time from the pipeline
            if response != 'Ready for next input':
                print(response)
            if response == ('bye bye'):
                return #have to return for both threads in order to fully end the client and gracefully exit
            #a large check to effectively see if the server is ready for a new input or if the client is receiving a tweet from a subscription
            if response != ('Ready for next input'): 
                if response != 'operation success' and response.find('operation failed') != 0 and not getTweetsWasUsed and not getUsersWasUsed and not subscribeWasUsed and (not response == ('bye bye') or not response == ('message length illegal, connection refused.') or not response == ('hashtag illegal format, connection refused.') or not response == ('error: username has wrong format, connection refused.')):
                    response = response[0:response.find(' ')] + ':' + response[response.find(' '):] #formats the tweet so that it is ready to be output with the timeline command
                    timeline.append(response)
                continue
            getTweetsWasUsed = False
            getUsersWasUsed = False
            subscribeWasUsed = False
            timelineWasUsed = False

    #thread for sending messages to the server
    def clientSendingThread():
        global timeline
        global getTweetsWasUsed
        global getUsersWasUsed
        global subscribeWasUsed
        global timelineWasUsed

        #the number of active subscriptions we have is checked client side
        numSubscriptions = 0


        while True:

            command = input('') #receive a command from the user

            commandLen = str(len(command))
            commandLen = commandLen.zfill(3) #the length of the command, which we append to the front when sent

            ###most error checking is done client side as well, such as parsing the message

            #tweet command
            if len(command) > 5 and command[0: 5] == ('tweet'):
                if len(command) < 7:
                    print('message length illegal, connection refused.')
                    s.send('005error'.encode()) #hard-coded lengths for hard-coded messages
                    continue
                messageAndHashTag = command[6:]
                if messageAndHashTag.find('\"') == messageAndHashTag.rfind('\"'):
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                message = messageAndHashTag[0:messageAndHashTag.rfind('\"') + 1]
                if len(message) > 152: #length 150 message + 2 quotes
                    print('message length illegal, connection refused.')
                    s.send('005error'.encode())
                    continue
                if len(message) < 3:
                    print('message format illegal.')
                    s.send('005error'.encode())
                    continue
                hashTags = messageAndHashTag[len(message):]
                if len(hashTags) == 0 or hashTags.find('##') > -1 or hashTags.count('#') > 5 or hashTags.find('#ALL') > -1:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                hashTags = hashTags[1:]
                allHashTags = hashTags.split('#') #more easily check the hashtags for correct formatting
                shouldExitCommand = False
                for hashTag in allHashTags:
                    if len(hashTag) > 14:
                        print('hashtag illegal format, connection refused.')
                        shouldExitCommand = True
                        break
                if shouldExitCommand:
                    s.send('005error'.encode())
                    continue
                s.send((str(commandLen) + command).encode())

            #subscribe command
            elif len(command) > 9 and command[0: 9] == ('subscribe'):
                if len(command) < 11:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                hashTag = command[10:]
                if numSubscriptions == 3:
                    print('operation failed: sub ' + hashTag + " failed, already exists or exceeds 3 limitation")
                    s.send('005error'.encode())
                    continue
                if len(hashTag) == 0 or not hashTag[0] == ('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                if len(hashTag) > 15:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                subscribeWasUsed = True
                s.send((str(commandLen) + command).encode())
                numSubscriptions = numSubscriptions + 1

            #unsubscribe command
            elif len(command) > 11 and command[0: 11] == ('unsubscribe'):
                if len(command) < 12:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                hashTag = command[12:]
                if len(hashTag) == 0 or not hashTag[0] == ('#') or hashTag.find('##') > -1 or hashTag.count('#') > 1:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                if len(hashTag) > 15:
                    print('hashtag illegal format, connection refused.')
                    s.send('005error'.encode())
                    continue
                s.send((str(commandLen) + command).encode())

            #timeline command
            elif command == ('timeline'):
                for tweet in timeline:
                    print(tweet)
                timelineWasUsed = True
                s.send((str(commandLen) + command).encode())

            #getusers command
            elif command == ('getusers'):
                getUsersWasUsed = True
                s.send((str(commandLen) + command).encode())



            #gettweets command
            elif len(command) > 9 and command[0:9] == ('gettweets'):
                if len(command) < 10:
                    print('error: username has wrong format, connection refused.')
                    s.send('timeline'.encode())
                    continue
                if not command[10:].isalnum():
                    print('error: username has wrong format, connection refused.')
                    s.send('timeline'.encode())
                    continue
                getTweetsWasUsed = True
                s.send((str(commandLen) + command).encode())

            #exit
            elif command == ('exit'):
                newCommand = command + ' ' + username #also send the username when exitting to make sure we logout the correct user
                newCommandLen = str(int(usernameLen) + int(commandLen) + 1)
                newCommandLen = newCommandLen.zfill(3)
                s.send((newCommandLen + newCommand).encode())
                return #have to return for both threads in order to fully end the client and gracefully exit

    #how we create 2 separate threads, one for receiving and one for sending messages
    t1 = threading.Thread(target=clientReceiveThread)
    t2 = threading.Thread(target=clientSendingThread)
    t1.start()
    t2.start()






if __name__ == '__main__':
    Main()