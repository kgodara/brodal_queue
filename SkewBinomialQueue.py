from heap_lib import node
from heap_lib import print_queue

class skew_binomial_queue:

    def __init__(self, rank, children):
        self.rank = rank
        self.children = children
        map((lambda x: x.parent(self)), self.children)
        self.children.sort(key=lambda x: x.rank, reverse=True)

    def get_root(self):
        return self.val

    def get_rank(self):
        return self.rank

    def get_min(self):
        smallest = node(0, float("inf"), [])
        for tree in self.children:
            if tree.val < smallest.val:
                smallest = tree
        return smallest

    def simple_link(self, tree1, tree2):

        if tree1.rank == tree2.rank:

            if tree1.val <= tree2.val:

                tree1.children.append(tree2)
                tree1.rank += 1

                index = 0

                iter_list = None
                if tree2.parent != None:
                    # print('ITER_LIST IS TREE2')
                    iter_list = tree2.parent
                else:
                    # print('ITER_LIST IS SELF`')
                    iter_list = self

                for idx, child in enumerate(iter_list.children):
                    if id(child) == id(tree2):
                        index = idx

                del iter_list.children[index]
                # iter_list.children.remove(iter_list.children[index])

                tree2.parent = tree1
                return 0

            else:

                tree2.children.append(tree1)
                tree2.rank += 1

                index = -1

                iter_list = None
                if tree1.parent != None:
                    iter_list = tree1.parent
                else:
                    iter_list = self

                for idx, child in enumerate(iter_list.children):
                    if id(child) == id(tree1):
                        index = idx

                del iter_list.children[index]

                tree1.parent = tree2
                return 1
        return -1

    def skew_link(self, tree0, tree1, tree2):
        assert(tree0.rank == 0 and tree1.rank == tree2.rank)
        # type B skew link
        if tree1.val < tree0.val and tree1.val < tree2.val:
            tree1.children.insert(0, tree2)
            tree1.children.insert(0, tree0)

            # possible_parent = tree0.parent
            index = -1
            if tree0.parent is not None:
                for idx, child in enumerate(tree0.parent.children):
                    if id(child) == id(tree0):
                        index = idx
                if index >= 0:
                    del tree0.parent.children[index]

            index = -1
            if tree2.parent is not None:
                for idx, child in enumerate(tree2.parent.children):
                    if id(child) == id(tree2):
                        index = idx
                if index >= 0:
                    del tree2.parent.children[index]
            else:
                self.children.remove(tree2)

            tree0.parent = tree1
            tree2.parent = tree1

            tree1.rank += 1

        elif tree2.val < tree0.val and tree2.val < tree1.val:
            tree2.children.insert(0, tree1)
            tree2.children.insert(0, tree0)

            # possible_parent = tree0.parent
            index = -1
            if tree0.parent is not None:
                for idx, child in enumerate(tree0.parent.children):
                    if id(child) == id(tree0):
                        index = idx
                if index >= 0:
                    del tree0.parent.children[index]

            index = -1
            if tree1.parent is not None:
                for idx, child in enumerate(tree1.parent.children):
                    if id(child) == id(tree1):
                        index = idx
                if index >= 0:
                    del tree1.parent.children[index]
            else:
                self.children.remove(tree1)

            tree0.parent = tree2
            tree1.parent = tree2

            tree2.rank += 1

        # type A skew link
        else:
            tree0.children.insert(0, tree1)
            tree0.children.insert(0, tree2)

            # possible_parent = tree0.parent

            index = -1
            if tree1.parent is not None:
                for idx, child in enumerate(tree1.parent.children):
                    if id(child) == id(tree1):
                        index = idx
                if index >= 0:
                    del tree1.parent.children[index]
            else:
                self.children.remove(tree1)

            index = -1
            if tree2.parent is not None:
                for idx, child in enumerate(tree2.parent.children):
                    if id(child) == id(tree2):
                        index = idx
                if index >= 0:
                    del tree2.parent.children[index]
            else:
                self.children.remove(tree2)

            tree1.parent = tree0
            tree2.parent = tree0

            tree0.rank += 1

    # add checks for if less than 2 trees in queue
    def insert(self, val):

        self.children.sort(key=lambda x: x.rank)
        insert_tree = node(0, val, [])

        two_smallest = [self.children[0], self.children[1]]
        if two_smallest[0].rank == two_smallest[1].rank:
            self.skew_link(insert_tree, two_smallest[0], two_smallest[1])

        elif two_smallest[0].rank != two_smallest[1].rank:
            self.children.append(insert_tree)
            # self.children.sort(key=lambda x: x.rank)
            insert_tree.parent = None
        self.rank = max(tree.rank for tree in self.children)+1
        self.children.sort(key=lambda x: x.rank, reverse=True)

    def meld_queue(self, new_queue, isTree=False):
        if isTree:
            self.children.append(new_queue)
        else:
            self.children.extend(new_queue.children)
        self.children.sort(key=lambda x: x.rank, reverse=True)

        i = 0
        while i < (len(self.children) - 1):

            if self.children[i].rank == self.children[i+1].rank:
                result = self.simple_link(self.children[i], self.children[i+1])
                # Prevents us from looping to -1, which ruins the whole meld
                if i > 0:
                    i -= 1
            else:
                i += 1
        self.rank = max(tree.rank for tree in self.children)+1

    def extract_min(self):
        smallest = self.get_min()
        self.children.remove(smallest)

        singletons = list()
        for child in smallest.children:
            if child.rank == 0:
                singletons.append(child)
                child.parent = None
                smallest.children.remove(child)

        for sub_queue in smallest.children:
            self.meld_queue(sub_queue, isTree=True)

        for singleton in singletons:
            self.insert(singleton.val)
        self.rank = max(tree.rank for tree in self.children)+1




# TEST / DEMO SECTION
tree0 = node(0, 4, [])
tree1 = node(1, 5, [node(0, 6, [])])
tree2 = node(2, 2, [node(1, 10, [node(0, 11, [])]), node(0, 9, [])])
tree3 = node(2, 7, [node(1, 8, [node(0, 9, [])]), node(0, 10, [])])

queue0 = skew_binomial_queue(3, [tree0, tree1, tree2])

print('QUEUE 1:')
print_queue(queue0)
print()

print('TRYING INSERT BELOW: ')
queue0.insert(12)
queue0.insert(13)
print_queue(queue0)

print('EXTRACT MIN:')
queue0.extract_min()
print_queue(queue0)
print()

print('MELD WITH TREE 3')
queue0.meld_queue(tree3, isTree=True)
print_queue(queue0)
