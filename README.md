# CS3251 Programming Assignment 2

## Authors: David Saiontz and Jackson Huffman

---

### How work was divided

Initially, we decided to divide the work with having David working on ttweetcli.py and Jackson work on ttweetser.py, so as to avoid stepping on each other's work and creating merge conflicts. We discussed, at a high level, how everything should work as well as how responses should be formatted. Once we had a baseline with all of the commands in each file, we worked together to squash bugs, each one taking on a different bug. We discussed how to fix the various bugs using Bluejeans, sharing our screens to give a better idea to our partner different ideas for how to deal with a bug.

Once an initial baseline for the commands was implemented, David implemented a solution to send the length of the message in the first 3 bytes of the message to keep the socket from attempting to get more bytes than are available in the pipeline, and Jackson implemented multi-threading in the client, using the existing code in the client and separating it into 2 different threads to support immediate arrival of subscribed tweets from the server. One thread is used for receiving messages from the server, and the other thread is used for sending messages to the server

After this, we both worked together to squash any bugs we found. 

---

### How to use our code

To use our code, first make sure you have installed python3. Once this is done, you can start the ttweetser.py by entering the following into terminal:

<code>python3 ttweetser.py \<ServerPort></code>

The tweetser.py does not have any commands that it can run, as it automatically processes inputs from clients.

To start ttweetcli.py, enter the following into terminal:

<code>python3 ttweetcli.py \<ServerIP> \<ServerPort> \<Username></code>

With tweetcli.py, you have 5 possible commands to use with it.

<code>tweet "message" #hash</code>

The first, the tweet command, allows a client to send a tweet, with message length < 150 characters, with hashtags each < 15 characters, and which has up to 5 hashtags. The tweet will be sent to the server, and the server will then immediately send the tweet to all users that are subscribed to any of the hashtags in the hashtag portion of the tweet. In addition, the tweet is saved on the server.

<code>subscribe #hash</code>

The next command allows a client to subscribe to the given hashtag, with hashtag <15 characters. The subscription is saved to the server, and whenever there is a tweet received with the given hashtag that is not from the same client, it will be sent automatically to the client.

<code>unsubscribe #hash</code>

The unsubscribe command allows a user to unsubscribe to the given hashtag, with length < 15 characters. The unsubscribe command is sent to the server, where the subscription to the given hashtag, if it is there, is removed. If the subscription does not exist, the command does not do anything.

<code>timeline</code>

The timeline command displays all tweets received by the server due to subscriptions. It will not display any tweets received by the server if it was sent via the "gettweets" command.

<code>getusers</code>

The getusers command displays all users that are currently online, including itself.

<code>gettweets \<Username></code>

The gettweets command will get all tweets sent by a given client with the given username. These tweets are not saved by the client for the timeline command, and will not be displayed by the timeline command unless they were also received due to a subscription.

<code>exit</code>

The exit command is first sent to the server, which cleans up any necessary states such as subscriptions and removes the client from the list of active users. Once completed, the server sends "bye bye", which signifies that the server has successfully removed the client from the list of active users, and the client then exits.

---

### Special Instructions

There are no special instructions, just make sure you have python3 installed and have your terminal pointing to the folder with our code.