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

    def is_root(self):
        return self.parent

    def getChildren(self):
        return [x.name for x in self.children]

def get_phase_0_tree():
    root = Directory('/', None, [])
    root.visited = True
    root_home = root.add('root')
    var = root.add('var')
    var_log = var.add('log')
    root_home.add('Documents')

    return root
