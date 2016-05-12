class Directory():
    def __init__(self, name, parent, children):
        self.name = name
        self.parent = parent
        self.children = children

    def add(self, name):
        dir = Directory(name, self.name, [])
        self.children.append(dir)
        return dir

    def is_root(self):
        return self.parent

def get_phase_0_tree(self):
    root = Directory('/', None, [])
    root_home = root.add('root')
    var = root.add('var')
    var_log = var.add('log')
    root_home.add('Documents')

    return root
