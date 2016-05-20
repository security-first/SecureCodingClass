# SecureCodingClass
This program goes hand in hand with a secure coding class and assists students in gaining hands-on experience with practicing the security concepts discussed.

This program is built as a server that emulates a linux command line session. Students connect to the server and learn the following concepts over the course of the various modules:
- Basic Networking
- Basic Linux commands (ls, cd, echo, cat)
- Principle of Least Privilege
- File Permissions
- Basic user management in Linux
- Password complexity requirements and why they are necessary
- SQL Injection (by injecting username/password fields)
- Shell commands and injecting code
- Buffer overflow vulnerabilities

Why not simply use Linux Virtual Machines and simple scripts?
Because Virtual Machines are prone to problems and bugs with configurations and installations. Moreover, it is impossible to track student progress when all of their work is done in a Virtual Machine. This program, with the accompanying teacher's dashboard, will maintain progress and records in real time so that teachers will know when to slow down and review and when to quickly proceed.

## Installation/Running the program
Requires: Python 2.7.8 (that is what it was developed in)
All modules used are native to python-2.7.8

Clone/Download the repository, open the folder, and run the main.py program
```
git clone https://github.com/security-first/SecureCodingClass.git
cd SecureCodingClass
python main.py
```

You should see the following in your terminal window:
```
Student socket now listening on port 8888
Waiting for accept
Serving Instructor dashboard on 127.0.0.1:8443
```
Note: the ports above are the default ports. The administrator/instructor dashboard is only available on the local machine. The student program is open to all interfaces. The default IP/interface and port number to listed for student connections can be configured via command line arguments.

## Phases
### Phase 0 (Basic Linux Navigation)
This phase tests the student's ability to successfully connect to a remote server via the command line. In addition, the linux commands "ls" and "cd" are tested by allowing the student a small directory structure to navigate. The phase concludes when the student successfully logs out.

### Phase 1 (Principle of Least Privilege)
This phase demonstrates the simple concept of "Principle of Least Privilege". Note with the students that they are currently logged into the server as the "root" or full administrator user. There is a new, confidential log file under /var/log/access_log.log that contains user's passwords and login records (not a best practice on its own, but we will return to that).  Students should display the log file with the new "cat" command. Then, the students should add a new user account using the "adduser" account. When they log back in as the new user, they should try to access the file and verify that the command now fails.

## Testing
You can use the test class "test.py" to run unit tests. As of this commit, the program was programmed and tested on Mac OSX 10.11.4.
```
python -m unittest test
```
