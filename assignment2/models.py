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
        new_node = Node(key=k,value=v)

        x = self.root
        y = None
        nodeToUpdate = []

        while x != None:
            nodeToUpdate.append(x)
            y = x 
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        new_node.p = y
        if y == None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else: 
            y.right = new_node
        
        for node in nodeToUpdate:
            node.size += 1


    def range(self, low, high):
        """
        The method should return a list of nodes whose key are in the range low
        to high (excluding low, including high)
        """
        result = []
        def rangeSearch(node,low,high):
            if node is None:
                return
            
            if node.key > low:
                rangeSearch(node.left,low,high)
            
            if node.key > low and node.key <= high:
                result.append(node)

            if node.key <= high:
                rangeSearch(node.right,low,high)

        rangeSearch(self.root,low,high)

        return result

    def select(self, k):
        """
        The method should return the node with rank k
        """
        def selectSearch(node,k):
            if node is None:
                return
            
            left_size = 0
            if node.left is not None: 
                left_size = node.left.size
            if left_size == k: 
                    return node
            elif left_size > k: 
                return selectSearch(node.left,k)
            else: 
                return selectSearch(node.right,k-left_size-1)
            
    
if __name__ == '__main__':
    # you can use this code to help test your implementation in the beginning
    arr = [15, 7, 19, 1, 4, 7, 14, 6, 10]

    tree = BinarySearchTree()
    for elm in arr:
        tree.insert(elm, elm)

    # this should print [1, 4, 6, 7, 10, 14, 15, 19]
    tree.print_sorted()

    print("________ RANGE test ________")
    result = tree.range(2,12)

    for elm in result:
        print(elm.key)
