#!/usr/bin/python
import logging
import directories, commands

logger = logging.getLogger('secure_class')


def phase0(connection, address, user):
    permitted_commands = ['ls', 'cd', 'exit']
    dir_tree = commands.DirectoryTree(directories.get_phase_0_tree())
    if len(user['Progress']) < 1:
        user['Progress'] = ['0 ls commands executed', '0 cd commands successfully executed']

    while True:
        connection.send("\n%s:%s$ " % (user['Name'].lower().replace(' ', ''), dir_tree.current_path()))
        parameters = connection.recv(100).strip()
        logger.info('Received from %s (%s): %s' % (user['Name'], address, parameters))
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
        logger.info('Received from %s (%s): %s' % (user['Name'], address, parameters))
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
                        target = parameters.split(' ')[1] # ignores any second, third, etc. parameters
                        result = dir_tree.cd(target)
                        if result:
                            connection.send(result)
                        else:
                            pass
                    else:
                        pass # in theory, this should return to the user's home directory
                elif command == 'adduser':
                    if len(parameters.split(' ')) > 1:
                        new_user = parameters.split(' ')[1]
                        result = dir_tree.adduser(user['Name'], new_user)
                        if result[0]:
                            # create home directory
                            user['Name'] = new_user.lower().replace(' ', '')
                            dir_tree.mkdir(user['Name'], parent='home')
                            temp = user['Progress'][1].split(' ')
                            temp[-1] = 'True'
                            user['Progress'][1] = ' '.join(temp)
                            connection.send(result[1])
                        else:
                            connection.send(result[1])
                elif command == 'cat':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1]
                        result = dir_tree.cat(target, user['Name'])
                        if 'AUTHENTICATION' in result:
                            temp = user['Progress'][0].split(' ')
                            temp[-1] = 'True'
                            user['Progress'][0] = ' '.join(temp)
                        connection.send(result)
                elif command == 'exit':
                    break
    return


def phase2(connection, address, user):
    permitted_commands = ['ls', 'cd', 'exit', 'adduser', 'cat', 'grep']
    username = user['Name'].lower().replace(' ', '')
    root = directories.get_phase_2_tree(username)
    dir_tree = commands.DirectoryTree(root, current=root.find_by_name(username))
    if 'Read Log file' in user['Progress'][0]:
        user['Progress'] = ['Found Hidden File: False', 'Found Hidden Password: False']

    while True:
        connection.send("\n%s:%s$ " % (username, dir_tree.current_path()))
        parameters = connection.recv(100).strip()
        logger.info('Received from %s (%s): %s' % (user['Name'], address, parameters))
        if parameters:
            print 'Received from client: %s' % parameters
            command = parameters.split(' ')[0]
            if not command in permitted_commands:
                connection.send('-bash: %s: command not found' % command)
            else:
                if command == 'ls':
                    if len(parameters.split(' ')) > 1 and parameters.split(' ')[1] == '-a':
                        results = '\n'.join(dir_tree.ls(hidden=True))
                        connection.send(results)
                        if '.secrets.txt' in results:
                            temp = user['Progress'][0].split(' ')
                            temp[-1] = 'True'
                            user['Progress'][0] = ' '.join(temp)
                    else:
                        connection.send('\n'.join(dir_tree.ls()))
                elif command == 'cd':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1] # ignores any second, third, etc. parameters
                        result = dir_tree.cd(target)
                        if result:
                            connection.send(result)
                        else:
                            pass
                    else:
                        pass # TODO: this should return to the user's home directory
                elif command == 'adduser':
                    if len(parameters.split(' ')) > 1:
                        new_user = parameters.split(' ')[1]
                        result = dir_tree.adduser(user['Name'], new_user)
                        connection.send(result[1])
                elif command == 'cat':
                    if len(parameters.split(' ')) > 1:
                        target = parameters.split(' ')[1]
                        result = dir_tree.cat(target, user['Name'])
                        connection.send(result)
                elif command == 'grep':
                    if len(parameters.split(' ')) == 3:
                        target_word = parameters.split(' ')[1]
                        target_file = parameters.split(' ')[2]
                        result = dir_tree.grep(target_word, target_file, user['Name'])
                        connection.send(result)
                        if 'password=securityisfun' in result:
                            temp = user['Progress'][1].split(' ')
                            temp[-1] = 'True'
                            user['Progress'][1] = ' '.join(temp)
                    else:
                        connection.send('usage: grep [pattern] [file ...]')
                elif command == 'exit':
                    break
    return
