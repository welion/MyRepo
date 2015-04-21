#-*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import sys

import argparse

host = 'localhost'

def echo_client(port):
	""" A simple echo client """
	#Create a TCP/IP socket
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, err_msg:
		print 'Socket creation failed. Error code: '+str(err_msg[0]) + ' Error msessage:' + str(err_msg[1])
		sys.exit()
	
	#Connect socket to the server
	server_address = (host, port)
	print "Connecting to %s port %s" % server_address
	sock.connect(server_address)

	#Send data
	try:
		message = "This is test message, it will be echoed"
		print "Sending message..."
		sock.sendall(message)
		#Look for the response
		amount_received = 0
		amount_excepted = len(message)
		while amount_received < amount_excepted:	
			data = sock.recv(16)
			amount_received += len(data)
			print "Recieved: %s" % data
	except socket.errno,e:
		print "Socket error: %s" % str(e)
	except Exception,e:
		print "Other excepiton: %s" % str(e)
	finally:
		print "Closing connection to the server"
		sock.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Socket Server example')
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	port = given_args.port
	echo_client(port)

	
