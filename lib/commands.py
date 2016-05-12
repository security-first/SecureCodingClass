class Directory_Tree():
    def __init__(self, directory):
        self.current = directory

    def current_path():
        path = [self.current.name]
        temp = self.current
        while not temp.parent or temp.parent == '/':
            temp = temp.parent
            path.insert(0, temp.name)
        path.insert(0, '')

    def ls(self):
        return self.current.children

    def cd(self, target):
        if '/' in target: # TO-DO
            return
        elif target == '.': # current directory
            return
        elif target == '..': # parent directory
            if not self.current.is_root():
                self.current = self.current.parent
            return
        elif target in self.current.children:
            self.current = self.current.children[self.current.children.index(target)]
