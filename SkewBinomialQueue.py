from Heap_Lib import node


class skew_binomial_queue:

    def __init__(self, rank, children):
        self.rank = rank
        self.children = children
        map((lambda x: x.parent=self), self.children)
        self.children.sort(key=lambda x: x.rank)

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

            index = -1
            if tree2.parent is not None:
                for idx, child in enumerate(tree2.parent.children):
                    if id(child) == id(tree2):
                        index = idx
                if index >= 0:
                    del tree2.parent.children[index]

            tree1.parent = tree0
            tree2.parent = tree0

            tree0.rank += 1



