#-*- coding; utf-8 -*-
#!/usr/bin/env python

import select
import socket
import os
import sys
import signal
import cPickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

# Some utilites
def send(channel, *args):
	buffer = cPickle.dumps(args)
	value = socket.htonl(len(buffer))
	size = struct.pack("L", value)
	channel.send(size)
	channel.send(buffer)

def receive(channel):
	size = struct.calcsize("L")  #Return size of C struct described by format string fmt "L"------>unsigned Long
	size = channel.recv(size)
	try:	
		size = socket.ntohl(struct.unpack("L", size)[0])
	except struct.error,e:
		return ''
	buf = ""
	while len(buf) < size:
		buf = channel.recv(size - len(buf))
	return cPickle.loads(buf)[0]

class ChatServer(object):
	""" An example chat server using select """
	def __init__(self, port, backlog=5):
		self.clients = 0
		self.clientmap = {}
		self.outputs = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((SERVER_HOST, port))
		print "Server listening on the port: %s..." % port
		self.server.listen(backlog)

		# Catch Keyboard interrupts
		signal.signal(signal.SIGINT, self.sighandler)

	def sighandler(self, signum, frame):
		"""clean up client outputs"""
		# close socket
		print 'Shuting down the server...'
		# Close existing client sockets
		for output in self.outputs:
			output.close()
		self.server.close()

	def get_client_name(self, client):
		""" Return client name """
		info = self.clientmap[client]
		host, name = info[0][0], info[1]
		return '@'.join(name, host)

	def run(self):
		inputs = [self.server, sys.stdin]
		self.outputs = []
		running = True
		while running:
			try:	
				readable, writeable, exceptional = select.select(inputs, self.outputs, [])
			except select.error, e:
				break

			for sock in readable:
				if sock == self.server:
					# handle the socket of server
					client, address = self.server.accept()
					print "Chat Server got connection from %d from %s" % (client.fileno(), address)
					
					# read the login name
					cname = receive(client).split('NAME: ')[1]

					# compute client name and send back
					self.clients += 1
					send(client, 'CLIENT: ' + str(address[0]))
					inputs.append(client)
					self.clientmap[client] = (address, cname)
					
					# Send join information to other clients
					msg = "\n(Connected: New client %d) from %s)" %(self.clients, self.get_client_name(client))
					for output in self.outputs:
						send(output,msg)
					self.output.append(client)

				elif sock == sys.stdin:
					# handle the stdin 
					junk = sys.stdin.readline()
					running = False

				else:
					# handle the other socket
					try:

						data = receive(sock)
						if data:
							# Send as new client's message...
							msg = '\n#[' + self.get_client_name(sock) +']>>' + data
							# Send data to all except server ourself
							for output in self.outputs:
								if output != sock:
									send(output, msg)
						else:
							print 'Chat server: %d hung up' % sock.fileno()
							self.clients -= 1
							sock.close()
							inputs.remove(sock)
							self.outputs.remove(sock)

							# Sending client leaving information to others
							msg = "\n(Now hung up: client from %s)" %self.get_client_name(sock)
							for output in self.outputs:
								send(output, msg)
					except socket.error, e:
						inputs.remove(sock)
						self.outputs.remove(sock)
		self.server.close()


class ChatClient(object):
	""" A command line chat client using select """
	
	def __init__(self, name, port, host = SERVER_HOST):
		self.name = name
		self.connected = None
		self.host = host
		self.port = port
		
		# Initial prompt
		self.prompt = '['  + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'
		
		# Connect to server
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((host, self.port))
			print "Now connected to the chat server@ port %d" % self.port
			self.connected = True
			
			# Send my name
			send(self.sock, 'NAME:' + self.name)
			data = receive(self.sock)
			
			# Contains client address, set it
			addr = data.split('CLIENT: ')[1]
			self.prompt = '[' + '@'.join((self.name, addr)) + ']>'
		except socket.error, e:
			print "Failed to connect to chat server @ port %d" % self.port
			sys.exit()

	def run(self):
		""" Chat client main loop """
		while self.connectted:
			try:
				sys.stdout.write(self.prompt)
				sys.stdout.flush()
				# Wait for input from stdin
				readable, writeable, exceptional = select.select([0,self.sock], [], [])
				for sock in readable:
					if sock == 0:
						data = sys.stdin.readline().strip()
						if data:
							send(self.sock, data)
					elif sock == self.sock:
						data = receive(self.sock)
						if not data:
							print 'Client shutting down.'
							self.connected = False
							break
						else:	
							sys.stdout.write(data + '\n')
							sys.stdout.flush()
			except KeyboardInterrupt:
				print " Client interrupted."
				self.sock.close()
				break

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Socket server example')
	parser.add_argument('--name', action="store", dest="name", required=True)
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	port = given_args.port
	name = given_args.name
	if name == CHAT_SERVER_NAME:	
		server = ChatServer(port)
		server.run()
	else:
		client = ChatClient(name=name, port=port)
		client.run()
