#-*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import socket

import threading
import SocketServer

SERVER_HOST = 'localhost'
SERVER_PORT = 0 		#Tell the kernel to pivk up a port dynamically
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkingClient():
	""" A client to test forking server """
	def __init__(self, ip, port):
		#Create a socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Connect to the server
		self.sock.connect((ip, port))

	def run(self):
		"""Clent playing with the server"""
		# Send data to the server
		current_process_id = os.getpid()
		print 'PID %s Sending message to the server: "%s" '% (current_process_id, ECHO_MSG)
		send_data_length = self.sock.send(ECHO_MSG)
		print 'Sent %d characters, so far...' % send_data_length
		
		#Display server response
		reponse = self.sock.recv(BUF_SIZE)
		print 'PID %s recevied: %s ' % (current_process_id, reponse[5:])

	def shutdown(self):
		self.sock.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		#Send echo back to the client
		data = self.request.recv(BUF_SIZE)
		current_process_id = os.getpid()
		response = '%s: %s' %(current_process_id, data)
		print "Server sending reponse [current_process_id: data] = [%s]" %response
		self.request.send(response)
		return

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer,):
	""" Nothing to add here, inherited everything necessary from parents"""
	pass

def main():
	# Lanch the server
	server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
	ip, port = server.server_address # Retrieve the port number
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.setDaemon(True) # don't hang on exit
	server_thread.start()
	print 'Server loop running PID: %s' % os.getpid()

	# Lanch the clients
	client1 = ForkingClient(ip, port)
	client1.run()

	
	client2 = ForkingClient(ip, port)
	client2.run()

	# Clean them up
	server.shutdown()
	client1.shutdown()
	client2.shutdown()
	server.socket.close()

if __name__ == '__main__':
	main()
	
