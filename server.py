#!/usr/bin/python

import time
import socket
import thread
import sys
import subprocess
import modules

s_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
registered_connections = {}

def start(host, port, connections):
    try:
        listen_for_connections(host, port, connections)
    except KeyboardInterrupt:
        print 'Exiting...'
        exit(0)

def listen_for_connections(host, port, connections):
    # Set up the socket
    s_main.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_main.bind((host, port))
    s_main.listen(connections)
    print 'Socket now listening on port %s' % port

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
                'Current Module': 0
            }
        thread.start_new_thread(handle_client, (conn_main,addr[0],))

def handle_client(conn_main, address):
    while conn_main:
        try:
            if registered_connections[address]['Current Module'] == 0:
                modules.phase0(conn_main, address)
        except socket.error:
            conn_main = None
            break
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
