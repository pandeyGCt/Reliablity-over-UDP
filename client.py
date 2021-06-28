'''
Saksham Pandey 2018A7PS0259H
Vanshaj Aggarwal 2018A7PS0309H
Arpit Adlakha 2018A7PS0250H
Surinder Singh Virk 2018A7PS0234H
Aditya Sharma 2018A7PS0315H
'''
import socket
import struct
import sys
import dataProcessor
import time
received=[]
packet_buffer=[]
expected=int(0)
'''
A basic UDP client
'''
def sendMessage(IP,Port,filename):
	global received,expected
	bytesToSend         = dataProcessor.convertString(20180259,filename)  #filename converting into packet
	serverAddressPort   = (IP, int(Port))  #server add
	bufferSize          = 1024 #buffer
	buffer_store=[]
	# Create a UDP et at client side
	with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:  #initialising socket
	# Send to server using created UDP et
		sock.settimeout(3) # setting socket timeout to 3 so that it times out if no contact is made by the server
		while True:
			print("Sending file name to the server......")
			sock.sendto(bytesToSend, serverAddressPort)  #sending filename repeatedly so it gets transmitted in case of any problem
			try:
				arr,addr=sock.recvfrom(bufferSize)
				if arr:
					break
			except socket.error as e:
				print("trying to send again.......")
				continue
		start=time.time()		
				
		while True:  #when server sends anything, the client goes into this loop, note that first few packets would always be lost
			try:
				arr,addr = sock.recvfrom(bufferSize)
			except socket.error as e:
				print("Connection Timed out")  # if no packet is recieved for 3 seconds the client times out and looses connection to the server
				break
			seq,checksum=struct.unpack('II',arr[:struct.calcsize('II')])
			filedata=arr[struct.calcsize('II'):]  # reading from the packet
			if(checksum==dataProcessor.myCheckSum(filedata+bytes(seq))): # verifing data packet
				if seq in received:
					sock.sendto(dataProcessor.convertString(seq,'ACK'), serverAddressPort)
					continue
				received.append(seq)
				
				
				if(seq==expected):
					expected+=1
					buffer_store.append(filedata)
					print(seq,"received")
					i=0
					while i != len(packet_buffer):
						try:
							if packet_buffer[i][0]== expected :
								buffer_store.append(packet_buffer[i][1])
								print("+Adding from Buffer",packet_buffer[i][0])
								packet_buffer.pop(i)
								expected+=1
								i=0
							else:
								i+=1
						except IndexError as e:
							print(e)
							continue	
									
				else:
					if ((seq,filedata)) not in packet_buffer:
						packet_buffer.append((seq,filedata))
						print("-adding to buffer",seq)
				sock.sendto(dataProcessor.convertString(seq,'ACK'), serverAddressPort)
			elif(seq in received):
				sock.sendto(dataProcessor.convertString(seq,'ACK'), serverAddressPort)
	end=time.time()
	print("Time Taken:",end-start-3)
	target="downloaded"+filename
	f=open(target,'wb')
	print("writing file")
	for i in range (0,len(buffer_store)):
		f.write(buffer_store[i])
	return
