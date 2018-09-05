class node:

    def __init__(self, rank, val, children):
        self.val = val
        self.rank = rank
        self.children = children
        self.parent = None
        for child in children:
            child.parent = self

    def set_parent(self, parent):
        self.parent = parent

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return '[rank=' + str(self.rank)+', val=' + str(self.val) + ']'

    def __str__(self):
        return '[rank=' + str(self.rank)+', val=' + str(self.val) + ']'