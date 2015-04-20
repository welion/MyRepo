#-*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import socket
import sys

def scan_ports(host,start_port,end_port):
	"""Scan remote host"""
	#Create socket
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	except socket.error.err_msg:
		print 'Socket creation failed. Error code: '+ str(err_msg[0]) + 'Error message: ' + str(err_msg[1])
		sys.exit()
	
	#Get IP of remote host
	try:
		remote_host = socket.gethostbyname(host)
	except socket.error,error_msg:
		print error_msg
		sys.exit()

	#Scan port
	end_port += 1
	for port in range(start_port,end_port):
		try:
			sock.connect((remote_host,port))
			print 'Port ' + str(port) + ' is open'
			sock.close()
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except socket.error:
			pass #skip various socket errors

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Remote Port Scanner')
	parser.add_argument('--host', action="store", dest="host", default="localhost")
	parser.add_argument('--start-port', action="store", dest="start_port", default=1, type=int)
	parser.add_argument('--end-port', action="store", dest="end_port", default=256, type=int)
	given_args = parser.parse_args()
	host,start_port,end_port = given_args.host, given_args.start_port, given_args.end_port
	scan_ports(host,start_port,end_port) 
