#!/usr/bin/python

import directories, commands

def phase0(connection, address, user):
    permitted_commands = ['ls', 'cd', 'exit']
    dir_tree = commands.DirectoryTree(directories.get_phase_0_tree())
    if len(user['Progress']) < 1:
        user['Progress'] = ['0 ls commands executed', '0 cd commands successfully executed']

    while True:
        connection.send("\nroot:%s$ " % dir_tree.current_path())
        parameters = connection.recv(100)
        parameters = parameters.strip()
        if parameters:
            print 'Received from client: %s' % parameters
            command = parameters.split(' ')[0]
            if not command in permitted_commands:
                connection.send('-bash: %s: command not found' % command)
            else:
                if command == 'ls':
                    connection.send('\n'.join(dir_tree.ls()))
                    user['Progress'][0] = '%s ls commands executed' % (int(user['Progress'][0].split(' ')[0]) + 1)
                elif command == 'cd':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1]
                        result = dir_tree.cd(target)
                        if result:
                            connection.send(result)
                        else:
                            user['Progress'][1] = '%s cd commands successfully executed' % (int(user['Progress'][1].split(' ')[0]) + 1)
                elif command == 'exit':
                    break
    return
