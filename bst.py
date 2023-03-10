# Name:Suhrob Hasanov
# OSU Email: hasanovs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4
# Due Date:
# Description: Implementing BST


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's value
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.
        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object, current_node=None) -> None:
        """
        This method adds new node to the tree
        """
        # If root is empty
        if self._root is None:
            self._root = BSTNode(value)
            # print(self.is_valid_bst())
            return
        node = self._root

        # If root is not empty
        while node is not None:
            if value < node.value:
                if node.left is None:
                    node.left = BSTNode(value)
                    # print(self.is_valid_bst())
                    return
                else:
                    node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(value)
                    # print(self.is_valid_bst())
                    return
                else:
                    node = node.right


    def find(self, value):
        """ Finds node with given value and returns boolean, node, its parent and its whether it right or left"""
        node = self._root
        parent_node = None
        child = None
        while node is not None:
            if node.value == value:
                # print(node, parent_node, child)
                return True, node, parent_node, child
            elif value < node.value:
                parent_node = node
                child = "left"
                node = node.left
            else:
                parent_node = node
                child = "right"
                node = node.right
        return False
    def inorder_successor_finder(self, node, parent_node=None):
        """ Finds in order successor and return along with its parent"""
        if node.right:
            if node.right.left:
                node = node.right
                parent_node = node
                # Keep looping till we get to leftmost
                while node.left is not None:
                    parent_node = node
                    node = node.left
                return node, parent_node
            else:
                # If no right left node
                return node.right, node
        elif node.left:
            return node.left, node
            # Must be a root node
        else:
            return None

    def remove(self, value: object) -> bool:
        """
        Removes node from the tree with the given value.
        """
        findResult = self.find(value)
        node = None
        parent_node = None

        if findResult:
            # Check and set for node
            if findResult[1]:
                node = findResult[1]
            # Node not found
            else:
                return False
            # Check and set parent node
            if findResult[2]:
                parent_node = findResult[2]

            whichChild = findResult[3]

        else:
            return False

        # In this block we are calling corresponding functions depending on child quantity
        if node.left is None and node.right is None:
            return self._remove_no_subtrees(parent_node, node, whichChild)
        elif node.left is None or node.right is None:
            return self._remove_one_subtree(parent_node, node, whichChild)
        elif node.left and node.right:
            return self._remove_two_subtrees(parent_node, node, whichChild)



    def _remove_no_subtrees(self, parent_node: BSTNode, node: BSTNode, whichChild) -> None:
        """
        Removes node if there are no subtrees
        """
        if parent_node:
            if whichChild == "left":
                parent_node.left = None
                return True
            # if node is parent's right child
            else:
                parent_node.right = None
                return True
        # If not parent and children, must be single root node
        elif parent_node is None:
            self._root = None
            return True


    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode, whichChild) -> None:
        """
        Removes node with one subtree
        """
        # remove node that has a left or right subtree (only)
        if remove_parent:
            # If remove is its parent's left child
            if whichChild == "left":
                # If the remove node does not have left child, but only right child
                if remove_node.left is None:
                    # Left child of parent becomes the right child of removed node
                    remove_parent.left = remove_node.right
                    return True
                elif remove_node.right is None:
                    # Left child of parent becomes the left child of removed node
                    remove_parent.left = remove_node.left
                    return True
            elif whichChild == "right":
                if remove_node.left is None:
                    remove_parent.right = remove_node.right
                    return True
                elif remove_node.right is None:
                    remove_parent.right = remove_node.left
                    return True
        # If no parent, must be root node with single subtree
        elif remove_parent is None:
            if remove_node.left:
                self._root = remove_node.left
                return True
            elif remove_node.right:
                self._root = remove_node.right
                return True


    def _remove_two_subtrees(self, parent_node: BSTNode, node: BSTNode, whichChild) -> None:
        """
        Removes node with two subtrees
        """

        # Establishing inorder successor and its parent
        inorder_successor_return = self.inorder_successor_finder(node)
        inorder_successor = inorder_successor_return[0]
        inorder_successor_parent = inorder_successor_return[1]

        # If node pas a parent
        if parent_node:
            # If node is its parent's left child
            if whichChild == "left":
                # No left node of parent
                if node.left is None:
                    if node.right.left is None:
                        parent_node.left = node.right
                        return True
                    elif node.right.left:
                        parent_node.left = inorder_successor
                        inorder_successor.right = node.right
                        node.right.left = inorder_successor.right
                        return True
                # Parent has a left node
                elif node.left:
                    if node.right.left is None:
                        parent_node.left = node.right
                        parent_node.left.left = node.left
                        return True
                    elif node.right.left:
                        parent_node.left = inorder_successor
                        inorder_successor.right = node.right
                        inorder_successor.left = node.left
                        node.right.left = inorder_successor.right
                        return True
            # If its parent's right child
            elif whichChild == "right":
                if node.left is None:
                    if node.right.left is None:
                        parent_node.right = node.right
                        return True
                    elif node.right.left:
                        parent_node.right = inorder_successor
                        inorder_successor.right = node.right
                        node.right.left = inorder_successor.right
                        return True
                elif node.left:
                    # print("elif node.left section ")
                    if node.right.left is None:
                        parent_node.right = node.right
                        node.right.left = node.left
                        return True
                    elif node.right.left:
                        parent_node.left = inorder_successor
                        inorder_successor.right = node.right
                        inorder_successor.left = node.left
                        node.right.left = inorder_successor.right
                        return True
        # If node does not have a parent
        elif parent_node is None:
            # If we have inorder successor, which is node.right.left node
            if node.right.left:
                if inorder_successor.left is None and inorder_successor.right is None:
                    self._root.value = inorder_successor.value
                    return True
                elif inorder_successor.left is None and inorder_successor.right:
                    # print("bottom")
                    inorder_successor.left = node.left
                    inorder_successor_parent.left = inorder_successor.right
                    inorder_successor.right = node.right
                    self._root = inorder_successor
                    return True
            # If we do not have inorder successor, which is node.right.left node
            elif node.right.left is None:
                inorder_successor.left = node.left
                self._root = inorder_successor
                return True


    def contains(self, value: object) -> bool:
        """
        Checks if node with given value in tree. Returns boolean
        """
        result = self.find(value)
        if result:
            return True
        else:
            return False

    def inorder_traversal(self, node=None) -> Queue:
        """
        Performs inorder traversal of the tree
        """
        return_queue = Queue()
        if self._root is None:
            return return_queue

        #  using helper function for processing
        self.in_order_helper(self._root, return_queue)
        return return_queue

    def in_order_helper(self, node: object, return_queue: object) -> None:
        """
        In order traversal method helper
        """
        # if node.left exists, go traversal to node.left then add current node
        if node.left is not None:
            self.in_order_helper(node.left, return_queue)
        # Add to queue node
        return_queue.enqueue(node.value)
        # if node.right exists, navigate traversal to node.right
        if node.right is not None:
            self.in_order_helper(node.right, return_queue)

    def find_min(self) -> object:
        """
        Returns the lowest value in tree
        """
        node = self._root
        # If tree is empty
        if node is None:
            return None
        # If no left child or right
        elif node.left is None and node.right is None:
            return node.value
        # If no left child
        elif node.left is None and node.right:
            node = node.right
            while node.left is not None:
                node = node.left
            if self._root.value < node.value:
                return self._root.value
            return node.value
        # If right child
        elif node.left:
            while node.left is not None:
                node = node.left
            if self._root.value < node.value:
                return self._root.value
            return node.value

    def find_max(self) -> object:
        """
        Returns the largest value in tree
        """
        node = self._root
        # If tree is empty
        if node is None:
            return None

        elif node.right is None:
            return node.value
        else:
            while node.right is not None:
                node = node.right
            return node.value

    def is_empty(self) -> bool:
        """
        Returns boolean depending if tree empty or not
        """
        if self._root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        Makes the tree empty
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    # print("\nPDF - method add() example 1")
    # print("----------------------------")
    # test_cases = (
    #     (1, 2, 3),
    #     (3, 2, 1),
    #     (1, 3, 2),
    #     (3, 1, 2),
    # )
    # for case in test_cases:
    #     tree = BST(case)
    #     print(tree)
    #
    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # test_cases = (
    #     (10, 20, 30, 40, 50),
    #     (10, 20, 30, 50, 40),
    #     (30, 20, 10, 5, 1),
    #     (30, 20, 10, 1, 5),
    #     (5, 4, 6, 3, 7, 2, 8),
    #     (range(0, 30, 3)),
    #     (range(0, 31, 3)),
    #     (range(0, 34, 3)),
    #     (range(10, -10, -2)),
    #     ('A', 'B', 'C', 'D', 'E'),
    #     (1, 1, 1, 1),
    # )
    # for case in test_cases:
    #     tree = BST(case)
    #     print('INPUT  :', case)
    #     print('RESULT :', tree)

    # print("\nPDF - method add() example 3")
    # print("----------------------------")
    # for _ in range(100):
    #     case = list(set(random.randrange(1, 20000) for _ in range(900)))
    #     tree = BST()
    #     for value in case:
    #         tree.add(value)
    #     if not tree.is_valid_bst():
    #         raise Exception("PROBLEM WITH ADD OPERATION")
    # print('add() stress test finished')


    # print("----------FIND START------------")
    # inputArray = (5, 4, 6, 3, 7, 2, 8)
    #
    # tree = BST()
    #
    # for item in inputArray:
    #     tree.add(item)
    # print(tree)
    #
    # print(tree.find(1))
    # print(tree.find(2))
    #
    # print(tree.find(0))
    # print(tree.find(99))
    # print(tree.remove(6))
    #
    #
    # print("----------FIND END------------")









    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        # ((1, 2, 3), 1),
        # ((1, 2, 3), 2),
        # ((1, 2, 3), 3),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((-93, 3, 70, -55, 49, -77, -7, 26, -69, -98), -93),
        ((3, -61, -57, 72, -20, -52, -47, -13, 25, -5), 3),
        ((-64, -63, -27, -83, -81, -15, -76, 86, 24), -64),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((96, 0, 70, -24, -88, 45, -82, 47, 17, -12), 96),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        # ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        # ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        # ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 3")
    print("---------------------------------")
    tree = BST( ["AQ", "SO", "QU", "G", "EF", "B", "C", "B", "B", "B", "B", "B", "B", "C",
     "DP","D", "DP", "E", "EF", "G", "NB", "HD", "G", "G", "G", "IG", "I", "HD", "IG", "L", "J", "K", "K", "OX", "P", "OX", "P", "RH", "R", "QU", "QU", "R", "R", "R", "R", "R", "R", "R", "S", "RH", "S", "TI", "T", "T", "Y", "XD", "TI", "Y", "Z", "Y", "ZL", "ZL"])
    print(tree)
    print("Minimum value is:", tree.find_min())




    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
