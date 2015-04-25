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

# 一些关键的辅助组件
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
	""" 使用select建立server"""
	def __init__(self, port, backlog):
		self.clients = 0
		self.clientmap = {}
		self.outputs = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.bind((SERVER_HOST, port))
		print "Server listening on the port: %s..." % port
		self.server.listen(backlog)

		# Catch Keyboard interrupts
		signal.signal(signal.SIGINT, self.sighandler)

	def sighandler(self, signum, frame):
		"""clean up client outputs"""
		# 关闭socket
		print 'Shuting down the server...'
		# 关闭所有已连接的client 的 socket
		for output in self.outputs:
			output.close()
		self.server.close()

	def get_client_name(self, client):
		""" 返回 client 的名称 """
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
					# 处理server的socket
					client, address = self.server.accept()
					print "Chat Server got connection from %d from %s" % (client.fileno(), address)
					
					# 获取登录的NAME
					cname = receive(client).split('NAME: ')[1]

					# 计算出NAME并回复信息
					self.clients += 1
					send(client, 'CLIENT: ' + str(address[0]))
					inputs.append(client)
					self.clientmap[client] = (address, cname)
					
					# 发送登录信息给其他client
					msg = "\n(Connected: New client %d) from %s)" %(self.clients, self.get_client_name(client))
					for output in self.outputs:
						send(output,msg)
					self.output.append(client)

				elif sock == sys.stdin:
					# 处理标准输入
					junk = sys.stdin.readline()
					running = False

				else:
					# 处理其他socket
					
