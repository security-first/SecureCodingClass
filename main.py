#!/usr/bin/python

import time
import socket
import thread
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
sys.path.insert(0, './lib') # inserting first to avoid name clashes
import modules

s_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
registered_connections = {}

class admin_server(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			user_data = ''
			for connection in registered_connections.keys():
				user_data += '''
					<tr>
						<td>{0}</td> <!-- Name -->
						<td>{1}</td> <!-- IP Address -->
						<td>{2}</td> <!-- Current Module -->
						<td><p>{3}</p></td> <!-- Progress -->
						<td>{4}</td> <!-- Last Activity -->
					</tr>
				'''.format( registered_connections[connection]['Name'],
                            connection,
                            'Module %s' % registered_connections[connection]['Current Module'],
                            '</p><p>'.join(registered_connections[connection]['Progress']),
                            registered_connections[connection]['Last-Activity'] )
			self.wfile.write(open('./http-files/index.html', 'r').read() % user_data)
		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(open('./http-files/404.html', 'r').read())
		return

def webserver():
	server_address = ('127.0.0.1', 8443) # Only available on the loopback interface - TO-DO: make port number customizable
	httpd = HTTPServer(server_address, admin_server)
	sa = httpd.socket.getsockname()
	print "Serving Instructor dashboard on %s:%s" % (sa[0], sa[1])
	httpd.serve_forever()
	return

def start(host, port, connections):
	try:
		thread.start_new_thread(webserver, ())
		listen_for_connections(host, port, connections)
	except KeyboardInterrupt:
		print 'Exiting...'
		exit(0)

def listen_for_connections(host, port, connections):
	# Set up the socket
	s_main.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s_main.bind((host, port))
	s_main.listen(connections)
	print 'Student socket now listening on port %s' % port

	# Loop forever while listening for incoming student connections
	while True:
		conn_main, addr = (None, None)

		print 'Waiting for accept'
		conn_main, addr = s_main.accept()
		print 'Handling new connection'
		print 'Connected with ' + addr[0] + ':' + str(addr)

		# "Sessions" are handled per IP Address. At the moment, therefore,
		# a connection from the same IP address is considered the same user
		if addr[0] in registered_connections.keys():
			registered_connections[addr[0]]['Last-Activity'] = time.strftime('%m/%d/%Y %H:%M:%S')
		else:
			registered_connections[addr[0]] = {
				'Current Module': 0,
                'Last-Activity': time.strftime('%m/%d/%Y %H:%M:%S'),
                'Progress': [],
				'Name': 'root',
			}
		thread.start_new_thread(handle_client, (conn_main,addr[0], registered_connections[addr[0]]))

def handle_client(conn_main, address, user):
	try:
		if registered_connections[address]['Current Module'] == 0:
			modules.phase0(conn_main, address, user)
			user['Current Module'] = 1
		elif registered_connections[address]['Current Module'] == 1:
			modules.phase1(conn_main, address, user)
			user['Current Module'] = 2
	except socket.error:
		pass
	registered_connections[address]['Last-Activity'] = time.strftime('%m/%d/%Y %H:%M:%S')
	print 'Disconnected from: %s' % address


def _print_usage(error=None):
	if error:
		print '[-] Error! %s' % error
	print 'Usage:\n./server.py [hostname] [port_number] [number_of_connections]'
	exit(0)

if __name__ == '__main__':
	default_port = 8888
	default_host = '127.0.0.1'
	default_connections = 10 # increase/specify per size of class

	#check for command line arguments to override default values
	if len(sys.argv) > 1:
		default_host = sys.argv[1]
		if len(sys.argv) > 2:
			try:
				default_port = int(sys.argv[2])
			except:
				_print_usage(error='Invalid value for port')
			if len(sys.argv) > 3: # arguments past the second are ignored
				try:
					default_connections = int(sys.argv[3])
				except:
					_print_usage(error='Invalid value for number of connections')

	start(default_host, default_port, default_connections)
