class Node:
    """
    This class represents a node in the tree with a key/value pair and
    optionally a pointer to its parent and its left and right child
    """
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.p = parent
        self.left = left
        self.right = right
        self.size = 1

    def __str__(self):
        return f'Node(key: {self.key}, val: {self.value})'

    def __repr__(self):
        return self.__str__()


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def print_sorted(self):
        """
        This is meant for early testing of your tree. It prints all the elements
        of the tree in a sorted order by calling the recursive method
        `_print_sorted`
        """
        self._print_sorted(self.root)

    def _print_sorted(self, x):
        """
        Recursively calls itself on the left subtree of `x`, then prints `x.key`
        and then calls itself on the right subtree of `x`
        """
        if x is not None:
            self._print_sorted(x.left)
            print(x.key)
            self._print_sorted(x.right)

    def insert(self, k, v):
        """
        IMPLEMENT THIS

        The arguments are some key `k` and some value `v` and the method should
        insert a new Node(k, v) into the tree
        """
        raise NotImplementedError

    def range(self, low, high):
        """
        IMPLEMENT THIS

        The method should return a list of nodes whose key are in the range low
        to high (excluding low, including high)
        """
        raise NotImplementedError

    def select(self, k):
        """
        IMPLEMENT THIS

        The method should return the node with rank k
        """
        raise NotImplementedError


if __name__ == '__main__':
    # you can use this code to help test your implementation in the beginning
    arr = [15, 7, 19, 1, 4, 7, 14, 6, 10]

    tree = BinarySearchTree()
    for el in arr:
        tree.insert(el, el)

    # this should print [1, 4, 6, 7, 10, 14, 15, 19]
    tree.print_sorted()
