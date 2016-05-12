#!/usr/bin/python

import directories, commands

def phase0(connection, address):
    permitted_commands = ['ls', 'cd']
    dir_tree = commands.Directory_Tree(directories.get_phase_0_tree())


    connection.send("root:%s$ " % dir_tree.current_path())
    parameters = connection.recv(100)
    parameters = parameters.strip()
    if parameters:
        print 'Received from client: %s' % parameters
        command = parameters.split(' ')[0]
        if not command in permitted_commands:
            connection.send('-bash: %s: command not found' % command)
        else:
            if command == 'ls':

    return
