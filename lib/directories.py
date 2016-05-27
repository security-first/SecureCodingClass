class File():
    def __init__(self, name, parent, contents, viewable_by_user):
        self.name = name
        self.parent = parent
        self.contents = contents
        self.viewed = False
        self.viewable_by_user = viewable_by_user

class Directory():
    def __init__(self, name, parent, children):
        self.name = name
        self.parent = parent
        self.children = children
        self.visited = False

    def add(self, name):
        dir = Directory(name, self, [])
        self.children.append(dir)
        return dir

    def add_file(self, name, contents, viewable_by_user):
        file = File(name, self, contents, viewable_by_user)
        self.children.append(file)
        return file

    def is_root(self):
        return self.parent

    def getChildren(self):
        return [x.name for x in self.children]

    def find_by_name(self, name): # returns the first instance of a name match (can't handle duplicate directory/file names)
        if self.name == name:
            return self
        elif len(self.children) == 0:
            return None
        else:
            for child in self.children:
                if child.name == name:
                    return child
                else:
                    a = child.find_by_name(name)
                    if a:
                        return a
        return None

def get_phase_0_tree():
    root = Directory('/', None, [])
    root.visited = True
    root_home = root.add('root')
    var = root.add('var')
    var_log = var.add('log')
    root_home.add('Documents')

    return root

def get_phase_1_tree():
    root = Directory('/', None, [])
    root.visited = True
    root_home = root.add('root')
    root.add('home')
    var = root.add('var')
    var_log = var.add('log')
    var_log.add_file('access.log', '''

2016-04-03 14:13:34 [AUTHENTICATION] John Smith successfully logged in using the password "P@ssword!"
2016-04-03 15:16:12 [AUTHENTICATION] Mary Adams failed to log in using the password "securityR0cks!"
2016-04-03 15:16:34 [AUTHENTICATION] Mary Adams successfully logged in using the password "SecurityR0cks!"
2016-04-03 16:02:56 [AUTHENTICATION] Matthew Jones failed to log in using the password "B@ltim0re!"
2016-04-03 16:03:16 [AUTHENTICATION] Matthew Jones failed to log in using the password "Baltim0re!"
2016-04-03 16:03:45 [AUTHENTICATION] Matthew Jones failed to log in using the password "b@ltlm0re!"
2016-04-03 16:03:46 [AUTHENTICATION] Matthew Jones's account has been locked out -- 3 unsuccessful attempts

    ''', 'root')
    root_home.add('Documents')

    return root

def get_phase_2_tree(user_name):
    root = Directory('/', None, [])
    root.visited = True
    root_home = root.add('root')
    home = root.add('home')
    home.add(user_name)
    var = root.add('var')
    var_log = var.add('log')

    return root
