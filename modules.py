#!/usr/bin/python

import directories, commands

def phase0(connection, address, user):
    permitted_commands = ['ls', 'cd', 'exit']
    dir_tree = commands.DirectoryTree(directories.get_phase_0_tree())
    if len(user['Progress']) < 1:
        user['Progress'] = ['0 ls commands executed', '0 cd commands successfully executed']

    while True:
        connection.send("\n%s:%s$ " % (user['Name'].lower().replace(' ', ''), dir_tree.current_path()))
        parameters = connection.recv(100).strip()
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
                        target = parameters.split(' ')[1] # ignores second, third, etc. parameters
                        result = dir_tree.cd(target)
                        if result:
                            connection.send(result)
                        else:
                            user['Progress'][1] = '%s cd commands successfully executed' % (int(user['Progress'][1].split(' ')[0]) + 1)
                elif command == 'exit':
                    break
    return

def phase1(connection, address, user):
    permitted_commands = ['ls', 'cd', 'exit', 'adduser', 'cat']
    dir_tree = commands.DirectoryTree(directories.get_phase_1_tree())
    if 'ls commands' in user['Progress'][0]:
        user['Progress'] = ['Read Log file: False', 'Added Standard User: False']

    while True:
        connection.send("\n%s:%s$ " % (user['Name'].lower().replace(' ', ''), dir_tree.current_path()))
        parameters = connection.recv(100).strip()
        if parameters:
            print 'Received from client: %s' % parameters
            command = parameters.split(' ')[0]
            if not command in permitted_commands:
                connection.send('-bash: %s: command not found' % command)
            else:
                if command == 'ls':
                    connection.send('\n'.join(dir_tree.ls()))
                elif command == 'cd':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1] #ignores any second, third, etc. parameters
                        result = dir_tree.cd(target)
                        if result:
                            connection.send(result)
                        else:
                            pass
                    else:
                        pass # in theory, this should return to the user's home directory
                elif command == 'adduser':
                    pass # TO-DO
                elif command == 'cat':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1]
                        result = dir_tree.cat(target, user)
                        if 'AUTHENTICATION' in result:
                            temp = user['Progress'][0].split(' ')
                            temp[-1] = 'True'
                            user['Progress'][0] = ' '.join(temp)
                        connection.send(result)
                elif command == 'exit':
                    break
    return
