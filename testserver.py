'''
Saksham Pandey 2018A7PS0259H
Vanshaj Aggarwal 2018A7PS0309H
Arpit Adlakha 2018A7PS0250H
Surinder Singh Virk 2018A7PS0234H
Aditya Sharma 2018A7PS0315H
'''


import socket
import os.path
import struct
from os import path
import threading
import sys
import dataProcessor
import time

framesize=64
nextPack=0
frame=[]
p_array=[]
packSent=0
condition=threading.Condition()
myBuffer=1024
AckCount=[]

def createServer(IP,Port):
	'''
	In this method a server is created which recieves filename and sends it if the file is found.
	'''
	global p_array
	localIP     = IP
	localPort   = int(Port)
	msgFromServer       = "File does not exist"
	bytesToSend         = str.encode(msgFromServer)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind((localIP, localPort))
	print("UDP server up and listening")
	
	# Listen for incoming datagrams
	while(True):
		arr,clientaddress = sock.recvfrom(myBuffer)
		seq,checksum=struct.unpack('II',arr[:struct.calcsize('II')])
		message=arr[struct.calcsize('II'):]
		print(message)
		
		if path.exists(message.decode('UTF-8')):#checking if file exists in server directory
			p_array=dataProcessor.makePacketArr(message.decode('UTF-8'))
			eof=dataProcessor.convertString(len(p_array),'EOF')
			startSend(sock,clientaddress)
			sock.close()
			break
		else:
			print("file not found")
		print(message)
		print(clientaddress)
		# Sending a reply to client
		sock.sendto(str.encode(msgFromServer), clientaddress)

		
def sendFile(sock,clientaddress):
	'''
	This method is responsible for sending window of frams in the beginning and periodically 
	'''
	global frame, p_array,condition,nextPack,framesize,packSent,AckCount
	while True :
		if len(AckCount) == len(p_array):
			break
		for i in range(0,len(frame)):
			try:
				sock.sendto(p_array[frame[i]],clientaddress)
			except IndexError as e:
				print(e)
				time.sleep(0.2)
				break
		with condition:
			time.sleep(0.1)
			
def recvAck(sock,clientaddress):
	'''
	This method recieves response from the client and adds a new frame to the window
	'''
	global frame,packsent,nextPack,p_array,myBuffer,AckCount
	while True :
		arr,add=sock.recvfrom(myBuffer)
		seq,checksum=struct.unpack('II',arr[:struct.calcsize('II')])
		filedata=arr[struct.calcsize('II'):]
		if not(seq in frame):
			print("corrupted/de-framed seq number")
			continue
		#elif (filedata.decode()=='ACK'):
		print("Got Ack ",seq)
		frame.remove(seq)
		if seq not in AckCount:
			AckCount.append(seq)
		if len(AckCount)== len(p_array):
			break
		if nextPack < len(p_array):
			try:
				sock.sendto(p_array[nextPack],clientaddress)
				frame.append(nextPack)
				nextPack+=1
			except IndexError as e:
				print(e)
				print(nextPack)
				continue
			except socket.error as e:
				print("trying to send again")
				continue
		else :
			continue

def startSend(sock,clientaddress):
	global frame,framesize,nextPack
	nextPack=0
	for i in range(0,framesize):
		if i == len(p_array) :
			break
		frame.append(i)
		nextPack=i+1
	t1=threading.Thread(target=sendFile,args=(sock,clientaddress))
	t2=threading.Thread(target=recvAck,args=(sock,clientaddress))
	print("starting t1")
	t1.start()
	print("starting t2")
	t2.start()
	t1.join()
	t2.join()
	print("transfer Completed")
	
def main():
	createServer()
	
if __name__ == "__main__":
    main()
