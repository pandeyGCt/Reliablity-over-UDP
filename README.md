'''
Saksham Pandey 2018A7PS0259H
Vanshaj Aggarwal 2018A7PS0309H
Arpit Adlakha 2018A7PS0250H
Surinder Singh Virk 2018A7PS0234H
Aditya Sharma 2018A7PS0315H
'''

TO RUN THE PROGRAM
1. keep the the files to be transfered in the same folder as the server
2. To run server enter command: python serverapp.py <server address> <server port>
3. To run the client enter commond: python client.py <server address> <server port> <file name to be requested>
4. The code runs and the file gets downloaded in the client folder

Changes to the protocol
1. Server instead of sending file list just receives a single filename from client
2. Not starting timer in server, created process which works similar
3. Instead of sending a Nack the client just ignores the corrupted packet and then the server retransmits it since the ack was not received.
