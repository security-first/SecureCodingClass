class DirectoryTree():
    def __init__(self, directory):
        self.current = directory

    def current_path(self):
        path = [self.current.name]
        temp = self.current
        while temp.parent and not temp.parent.name == '/':
            temp = temp.parent
            path.insert(0, temp.name)
        return '/'.join(path)

    # Emulates the basic "ls" linux command (without flags)
    # Input: None
    # Output: Returns all of the children names of the current directory
    def ls(self):
        return [x.name for x in self.current.children]

    def cd(self, target):
        print '[*] Attempting to change from %s to %s' % (self.current.name, target)
        if '/' in target: # TO-DO
            temp = self.current
            for dir in target.split('/'):
                if dir == '.':
                    continue
                elif dir == '..':
                    if not temp.is_root():
                        temp = temp.parent
                    else:
                        continue
                else:
                    if dir in self.current.getChildren():
                        temp = self.current.children[self.current.children.index(dir)]
                    else:
                        return '-bash: cd: %s: No such file or directory' % target
            return None
        elif target == '.': # current directory
            pass
        elif target == '..': # parent directory
            if not self.current.is_root():
                self.current = self.current.parent
        elif target in self.current.getChildren():
            found = False
            for child in self.current.children:
                if child.name == target:
                    self.current = child
                    found = True
            if not found:
                return '-bash: cd: %s: No such file or directory' % target
        print '[*] Now in directory: %s' % self.current.name
        self.current.visited = True
        return None
    
