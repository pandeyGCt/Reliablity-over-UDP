'''
Saksham Pandey 2018A7PS0259H
Vanshaj Aggarwal 2018A7PS0309H
Arpit Adlakha 2018A7PS0250H
Surinder Singh Virk 2018A7PS0234H
Aditya Sharma 2018A7PS0315H
'''
import struct
import socket
from array import array

def myCheckSum(data):
    if len(data) % 2:
        data += b'\x00'
    s = sum(array('H',data))
    s = (s & 0xffff) + (s >> 16)
    s += (s >> 16)
    return socket.ntohs(~s & 0xffff)

def getFileData(name):
	'''
	This method gets the data and breaks it into chunks.
	'''
	try:
		f=open(name,"rb")
		file_data=f.read()
		file_data_size=len(file_data)
		pack_size=1000
		data=[]
		for i in range(0,file_data_size,pack_size):
			if(file_data_size-i>pack_size):
				data.append(file_data[i:i+pack_size])
			else:
				data.append(file_data[i:file_data_size])
		return data
	except IOError:
		print("Filen not found or incorrect path")
	finally:
		print("EXIT")
			
			
def makePacketArr(name):
	'''
	This method creates a list containing packets to be sent.
	'''
	data=getFileData(name)
	packet_array=[]
	for i in range(0,len(data)):
		packer = struct.Struct('I I {}s'.format(len(data[i])))
		frame=(i,myCheckSum(data[i]+bytes(i)),data[i])
		packet_array.append(packer.pack(*frame))
	return packet_array

def convertString(seq,string):
	'''
	This method creates a given seq and string into a packet to be sent to the server
	'''
	string= string.encode('UTF-8')
	packer = struct.Struct('I I {}s'.format(len(string)))
	frame=(seq,myCheckSum(string),string)
	d=packer.pack(*frame)
	return d

def convertFilename(string):
	string=string.encode('UTF-8')
	packer=struct.Struct('I {}s'.format(len(string)))
	frame=(myCheckSum(string),string)
	d=packer.pack(*frame)
	return d
		
		
