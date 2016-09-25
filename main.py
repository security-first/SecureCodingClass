#!/usr/bin/python

import time
import socket
import thread
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
sys.path.insert(0, './lib') # inserting first to avoid name clashes
import modules

s_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
registered_connections = {}
logger = logging.getLogger('secure_class')
logger.basicConfig(format='%(asctime)s - %(levelname): %(message)s',
					datefmt='%m/%d/%Y %I:%M:%S %p',
					filename='events.log',
					level=logging.DEBUG)


# Purpose: Defines server for presenting student data (i.e. progress through the modules, activity, etc.)
class AdminServer(BaseHTTPRequestHandler):
	# Handler for the GET requests
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


def _print(msg, level='INFO'):
	print msg
	if level == 'CRITICAL':
		logger.critical(msg)
	elif level == 'ERROR':
		logger.error(msg)
	elif level == 'WARNING':
		logger.warning(msg)
	elif level == 'DEBUG':
		logger.debug(msg)
	else:
		logger.info(msg)

def webserver():
	server_address = ('127.0.0.1', 8443) # Only available on the loopback interface - TODO: make port number customizable
	httpd = HTTPServer(server_address, AdminServer)
	sa = httpd.socket.getsockname()
	_print("Serving Instructor dashboard on %s:%s" % (sa[0], sa[1]), level='DEBUG')
	httpd.serve_forever()
	return


def start(host, port, connections):
	try:
		thread.start_new_thread(webserver, ())
		listen_for_connections(host, port, connections)
	except KeyboardInterrupt:
		_print('Exiting...')
		exit(0)


def listen_for_connections(host, port, connections):
	# Set up the socket
	s_main.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s_main.bind((host, port))
	s_main.listen(connections)
	_print('Student socket now listening on port %s' % port, level='DEBUG')

	# Loop forever while listening for incoming student connections
	while True:
		conn_main, addr = (None, None)

		_print('Waiting for accept')
		conn_main, addr = s_main.accept()
		_print('Handling new connection')
		_print('Connected with ' + addr[0] + ':' + str(addr))

		# "Sessions" are handled per IP Address. At the moment, therefore,
		# a connection from the same IP address is considered the same user
		if addr[0] in registered_connections.keys():
			registered_connections[addr[0]]['Last-Activity'] = time.strftime('%m/%d/%Y %H:%M:%S')
			logger.info('Handling new connection from %s (%s)' % (addr[0], registered_connections[addr[0]]['Name']))
		else:
			registered_connections[addr[0]] = {
				'Current Module': 0,
				'Last-Activity': time.strftime('%m/%d/%Y %H:%M:%S'),
				'Progress': [],
				'Name': 'root',
			}
			logger.info('Creating new user for connection from %s' % addr[0])
		thread.start_new_thread(handle_client, (conn_main,addr[0], registered_connections[addr[0]]))


# I: Connection handler, IP Address, and User Data
# O: Configures the appropriate module per user
def handle_client(conn_main, address, user):
	try:
		if registered_connections[address]['Current Module'] == 0:
			modules.phase0(conn_main, address, user)
		elif registered_connections[address]['Current Module'] == 1:
			modules.phase1(conn_main, address, user)
		elif registered_connections[address]['Current Module'] == 2:
			modules.phase2(conn_main, address, user)

		user['Current Module'] += 1
		logger.info('%s (%s) has advanced to module %s' % (user['Name'], address, user['Current Module']))
	except socket.error:
		pass
	registered_connections[address]['Last-Activity'] = time.strftime('%m/%d/%Y %H:%M:%S')
	_print('Disconnected from: %s' % address)


# I: Error message, defaults to None
# O: Prints error message, if provided, usage message, and exits
def _print_usage(error=None):
	if error:
		_print('[-] Error! %s' % error, level='ERROR')
	print 'Usage:\n./server.py [hostname] [port_number] [number_of_connections]'
	exit(0)

# Main method -- Entry Point
if __name__ == '__main__':
	default_port = 8889
	default_host = '127.0.0.1'
	default_connections = 10 # increase/specify per size of class

	# check for command line arguments to override default values
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
				except ValueError:
					_print_usage(error='Invalid value for number of connections')

	start(default_host, default_port, default_connections)
