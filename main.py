# basic node structure
from datetime import time


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None

    # insert element into tree
    # splay the tree
    # @param element - item to be inserted
    # @returns 0 on success, -1 on failure, tree
    def insert(self, element):
        # if tree is empty
        if self.root is None:
            self.root = Node(element)
            return 0

        parent_node = self.root
        new_node = Node(element)

        # insert new element, same as BST
        while True:
            if element < parent_node.value:
                if parent_node.left is not None:
                    parent_node = parent_node.left
                else:
                    parent_node.left = new_node
                    new_node.parent = parent_node
                    break
            elif element > parent_node.value:
                if parent_node.right is not None:
                    parent_node = parent_node.right
                else:
                    parent_node.right = new_node
                    new_node.parent = parent_node
                    break
            elif element == parent_node.value:
                return -1

        return self.splay(new_node)

    # search the tree for element
    # splay the tree
    # @param element - item to be searched for
    # @returns element found - the root of the tree
    #          -1 when item is not in tree
    def search(self, element):
        current = self.root
        while True:
            if element == current.value:
                return self.splay(current)
            elif element < current.value:
                if current.left is not None:
                    current = current.left
                else:
                    return -1
            elif element > current.value:
                if current.right is not None:
                    current = current.right
                else:
                    return -1

    # search the tree for element
    # splay the element
    # remove element
    # join trees
    # @param element - item to be deleted
    # @returns tree after deletion
    def delete(self, element):
        # find element in tree and splay to root if found
        return_value = self.search(element)
        if return_value == -1:  # element is not in tree
            return -1
        # else split to two subtrees and join into one
        left_subtree = self.root.left
        right_subtree = self.root.right
        return self.join(left_subtree, right_subtree)

    # join two subtrees in one tree
    # play the largest node in tree I, append tree II as right child
    # @returns 0 on success, -1 on failure
    def join(self, root_I, root_II):
        if root_I is None:
            return root_II
        if root_II is None:
            return root_I

        max_element = self.find_maximum(root_I)
        root_I = root_I.splay(max_element)

        self.root = root_I
        root_II.parent = root_I
        self.root.right = root_II
        return self.root

    # splay accessed element to the root of the tree
    # uses right, left rotations
    # @param element - element to be splayed
    # @returns 0 on success, -1 on failure, time lapsed, tree
    def splay(self, node):
        while node.parent:
            parent = node.parent
            if not parent.parent:
                if node == parent.left:
                    self.right_rotate(node)
                else:
                    self.left_rotate(node)
            elif node == parent.left and parent == parent.parent.left:  # right - right
                self.right_rotate(parent)
                self.right_rotate(node)
            elif node == parent.right and parent == parent.parent.right:  # left - left
                self.left_rotate(parent)
                self.left_rotate(node)
            elif node == parent.right and parent == parent.parent.left:  # left - right
                self.left_rotate(node)
                self.right_rotate(node)
            else:
                self.right_rotate(node)  # right - left
                self.left_rotate(node)
        self.root = node
        return self.root

    # helper function, rotate node left
    def left_rotate(self, node):
        parent_node = node.parent
        parent_node.right = None
        node.parent = parent_node.parent
        if parent_node.parent:
            if parent_node == parent_node.parent.left:
                parent_node.parent.left = node
            else:
                parent_node.parent.right = node

        if node.left is None:
            parent_node.parent = node
            node.left = parent_node
        else:
            left_tmp = node.left
            parent_node.parent = node
            node.left = parent_node
            parent_node.right = left_tmp
            left_tmp.parent = parent_node

    # helper function, rotate node right
    def right_rotate(self, node):
        parent_node = node.parent
        parent_node.left = None
        node.parent = parent_node.parent
        if parent_node.parent:
            if parent_node == parent_node.parent.left:
                parent_node.parent.left = node
            else:
                parent_node.parent.right = node

        if node.right is None:
            parent_node.parent = node
            node.right = parent_node
        else:
            right_tmp = node.right
            parent_node.parent = node
            node.right = parent_node
            parent_node.left = right_tmp
            right_tmp.parent = parent_node

    def find_maximum(self, root):
        if root is None:
            return None
        current = root
        while current.right:
            current = current.right
        return current


def construct_tree(items):
    new_tree = SplayTree()
    for element in items:
        new_tree.insert(element)
    return new_tree


if __name__ == '__main__':
    # timer
    start_time = time.time()

    # items = [8, 2, 4, 3, 11, 9]
    # tree = construct_tree(items)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time:.2f}")
    