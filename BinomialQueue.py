from heap_lib import node


class binomial_queue:

    def __init__(self, rank, children):
        self.rank = rank 
        self.children = children
        map((lambda x: x.set_parent(self)), self.children)
        self.children.sort(key=lambda x: x.rank)

    def get_root(self):
        return self.val

    def get_rank(self):
        return self.rank

    def link(self, tree1, tree2):

        if tree1.rank == tree2.rank:

            if tree1.val <= tree2.val:

                tree1.children.append(tree2)
                tree1.rank += 1

                index = 0

                iter_list = None
                if tree2.parent != None:
                    iter_list = tree2.parent
                else:
                    iter_list = self

                for idx, child in enumerate(iter_list.children):
                    if id(child) == id(tree2):
                        index = idx

                del iter_list.children[index]

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

    def insert(self, val):
        insert_tree = node(0, val, [])
        sameRank = False
        self.children.append(insert_tree)
        self.children.sort(key=lambda x: x.rank)
        insert_tree.parent = None

        self.insert_helper(insert_tree)

    def insert_helper(self, insert_tree):

        iter_list = None
        if insert_tree.parent != None:
            iter_list = insert_tree.parent
        else:
            iter_list = self

        for sibling in iter_list.children:

            sibling_list = None
            if sibling.parent != None:
                sibling_list = sibling.parent
            else:
                sibling_list = self

            if sibling.rank == insert_tree.rank:

                if(id(sibling) != id(insert_tree)):
                    elevated_rank = self.link(sibling, insert_tree)
                    if elevated_rank == 0:
                        children = sibling_list.children
                        elevated_rank = sibling.rank
                    else:
                        children = iter_list.children
                        elevated_rank = insert_tree.rank

                    for tree in children:
                        if tree.rank == elevated_rank:
                            self.insert_helper(tree)
                            break

    def meld_queue(self, new_queue):
        self.children.extend(new_queue.children)
        self.children.sort(key=lambda x: x.rank)

        i = 0
        while i < (len(self.children) - 1):

            if self.children[i].rank == self.children[i+1].rank:
                result = self.link(self.children[i], self.children[i+1])
                # Prevents us from looping to -1, which ruins the whole meld
                if i > 0:
                    i -= 1
            else:
                i += 1

    def get_min(self):
        smallest = node(0,float("inf"), [])
        for tree in self.children:
            if tree.val < smallest.val:
                smallest = tree
        return smallest

    def extract_min(self):
        smallest = self.get_min()
        meld_queue = binomial_queue(smallest.rank, smallest.children)
        self.children.remove(smallest)
        self.meld_queue(meld_queue)

    def print_queue(self):

        print('[rank=' + str(self.rank) + ']')

        if self.rank > 0:
            for tree in self.children:
                self.print_helper(1, tree)

    def print_helper(self, depth, tree):

        print(('  '*depth) + '[rank=' + str(tree.rank)+', val=' + str(tree.val) + ']')

        if tree.rank > 0:
            for tree in tree.children:
                self.print_helper(depth + 1, tree)


# TEST / DEMO SECTION
tree0 = node(0, 4, [])
tree1 = node(1, 5, [node(0, 6, [])])
tree2 = node(2, 8, [node(1, 10, [node(0, 11, [])]), node(0, 9, [])])

queue0 = binomial_queue(3, [tree0, tree1, tree2])

print('QUEUE 1:')
queue0.print_queue()
print()

print('TRYING INSERT BELOW: ')
queue0.insert(12)
queue0.print_queue()
print()

tree3 = node(0, 7, [])
tree4 = node(1, 13, [node(0, 17, [])])
queue1 = binomial_queue(2, [tree3, tree4])
print('QUEUE 2:')
queue1.print_queue()
print()

queue0.meld_queue(queue1)
print('MELDED QUEUE:')
queue0.print_queue()
print()

print('EXTRACT MIN:')
queue0.extract_min()
queue0.print_queue()
print()
