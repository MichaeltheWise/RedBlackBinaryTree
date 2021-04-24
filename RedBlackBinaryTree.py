# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 2021

@author: Michael Lin
"""
import collections


class Node:
    def __init__(self, val):
        super(Node, self).__init__()
        self.parent = None
        self.left = None
        self.right = None
        self.val = val
        # Default red as 1 and black as 0
        self.color = 1


class RedBlackBinaryTree:
    def __init__(self):
        super(RedBlackBinaryTree, self).__init__()
        # Need to create a new type of node called null_node
        # This null_node is basically None but it has black color coded
        self.null_node = Node(0)
        self.null_node.color = 0
        self.null_node.left = None
        self.null_node.right = None

        # Assign root as a null node first
        self.root = self.null_node

    def __contains__(self, key):
        return self.find(key)

    def insert(self, num):
        """
        Binary tree insertion
        :param num: number to be inserted
        :return: None
        """
        # Create the new node
        new_node = Node(num)
        new_node.left = self.null_node
        new_node.right = self.null_node

        # This implementation is different from the recursion method implemented in BinaryTree
        # Traversing while keeping track of parent
        parent = None
        curr = self.root
        while curr != self.null_node:
            parent = curr
            if new_node.val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        new_node.parent = parent

        # Insert the node after we reach the bottom of the tree
        # Compare with parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

        # Exit check before re-balancing
        # If root, double checking that the node has color black
        if new_node.parent is None:
            new_node.color = 0
            return

        # if grandparent doesn't exist, just return
        if new_node.parent.parent is None:
            return

        self.insert_rebalance(new_node)

    def insert_rebalance(self, node):
        """
        Rebalance the color after insertion
        :param node: current node
        :return: None
        """
        # If parent is red
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                # Find the uncle
                uncle = node.parent.parent.left

                # CASE 1: if parent not black and not root, uncle is red
                # Flip uncle, parent and grandparent color, then repeat upward
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    # CASE 2: if parent not black and not root, uncle is black
                    # RL case
                    # Need to transition to RR case
                    if node == node.parent.left:
                        node = node.parent
                        # Need to swap from left leg to right leg
                        self.right_rotate(node)
                    # CASE 3: if parent not black and not root, uncle is black
                    # RR case
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    # Then we left rotate
                    self.left_rotate(node.parent.parent)

            else:
                # uncle on the other side
                uncle = node.parent.parent.right

                # CASE 1: if parent not black and not root, uncle is red
                # Flip uncle, parent and grandparent color, then repeat upward
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    # CASE 4: if parent not black and not root, uncle is black
                    # LR case
                    # Need to transition to LL case
                    if node == node.parent.right:
                        node = node.parent
                        # Need to swap from right leg to left leg
                        self.left_rotate(node)
                    # CASE 5: if parent not black and not root, uncle is black
                    # LL case
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    # Then we right rotate
                    self.right_rotate(node.parent.parent)

            # If we reach root, stop
            if node == self.root:
                break

        # After CASE 1, there is the possibility that the root has been recolored to red
        # To ensure that red black tree property is secured, repaint to black
        self.root.color = 0

    def right_rotate(self, node):
        """
        Right rotation
        :param node: node
        :return: None
        """
        # Child rotation
        # Sibling transfers to grandparent's left side
        tmp = node.left
        node.left = tmp.right
        if tmp.right != self.null_node:
            # Make sure child's parent is assigned from parent to grandparent
            tmp.right.parent = node

        # Parent reassignment
        tmp.parent = node.parent
        if node.parent is None:
            self.root = tmp
        elif node == node.parent.left:
            # Figure out whether the node is its parent's left or right child then assign
            node.parent.left = tmp
        else:
            node.parent.right = tmp

        # Actual rotation
        tmp.right = node
        node.parent = tmp

    def left_rotate(self, node):
        """
        Left rotation
        :param node: node
        :return: None
        """
        # Child rotation
        # Sibling transfers to grandparent's right side
        tmp = node.right
        node.right = tmp.left
        if tmp.left != self.null_node:
            # Make sure child's parent is assigned from parent to grandparent
            tmp.left.parent = node

        # Parent reassignment
        tmp.parent = node.parent
        if node.parent is None:
            self.root = tmp
        elif node == node.parent.left:
            # Figure out whether the node is its parent's left or right child then assign
            node.parent.left = tmp
        else:
            node.parent.right = tmp

        # Actual rotation
        tmp.left = node
        node.parent = tmp

    def delete(self, node, num):
        """
        Implementation of removal
        :param node: node
        :param num: number to be removed
        :return: None
        """
        # Replicate the find function here for further operation after finding the match
        curr = self.null_node
        while node != self.null_node:
            if node.val == num:
                curr = node
            if node.val > num:
                node = node.left
            else:
                node = node.right

        if curr == self.null_node:
            print("Node not found")
            return

        tmp = curr
        tmp_color = tmp.color
        # Basic removal with one child or zero child
        if curr.left == self.null_node:
            # Replace with right if left empty
            replacement = curr.right
            self._parent_reassign(curr, curr.right)
        elif curr.right == self.null_node:
            # Replace with right if left empty
            replacement = curr.left
            self._parent_reassign(curr, curr.left)
        else:
            # Removal with two children
            tmp = self._minVal(curr.right)
            tmp_color = tmp.color
            replacement = tmp.right
            if tmp.parent == curr:
                # If the minimum value is right below the node to be deleted, simple replacement
                replacement.parent = tmp
            else:
                self._parent_reassign(tmp, tmp.right)
                tmp.right = curr.right
                tmp.right.parent = tmp

            self._parent_reassign(curr, tmp)
            tmp.left = curr.left
            tmp.left.parent = tmp
            tmp.color = curr.color

        # Red black tree deletion balancing
        if tmp_color == 0:
            self.delete_rebalance(replacement)

    def delete_rebalance(self, node):
        # If node is double black situation
        while node != self.root and node.color == 0:
            if node == node.parent.left:
                # Find the sibling
                sibling = node.parent.right
                # CASE 1: if sibling is red
                # Adjustment, rotate then reassign sibling
                if sibling.color == 1:
                    sibling.color = 0
                    sibling.parent.color = 1
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                # CASE 2: if sibling is black and children are both black
                # Recoloring, recolor then proceed upward
                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    # CASE 3: if sibling is black and children have red
                    # Restructuring, LL, LR, RR, RL cases
                    if sibling.right.color == 0:
                        sibling.left.color = 0
                        sibling.color = 1
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = 0
                    sibling.right.color = 0
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                # CASE 1: if sibling is red
                # Adjustment, rotate then reassign sibling
                if sibling.color == 1:
                    sibling.color = 0
                    node.parent.color = 1
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                # CASE 2: if sibling is black and children are both black
                # Recoloring, recolor then proceed upward
                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    # CASE 3: if sibling is black and children have red
                    # Restructuring, LL, LR, RR, RL cases
                    if sibling.left.color == 0:
                        sibling.right.color = 0
                        sibling.color = 1
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = sibling.parent.color
                    node.parent.color = 0
                    sibling.left.color = 0
                    self.right_rotate(node.parent)
                    node = self.root
        # Make sure the root node is black
        node.color = 0

    def _parent_reassign(self, node1, node2):
        """
        Parent reassignment needed for removal
        :param node1: the node that is going to be deleted
        :param node2: the node replacing it
        :return: None
        """
        if node1.parent is None:
            self.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node1.parent = node2.parent

    def _minVal(self, node):
        """
        Find the minimum value down the tree
        :param node: node
        :return: the minimum value node
        """
        while node.left != self.null_node:
            node = node.left
        return node

    def find(self, num):
        """
        Binary tree search
        :param num: desired number
        :return: Boolean True/False or None
        """
        if self.root is not None:
            return self._find(self.root, num)
        else:
            return None

    def _find(self, node, num):
        """
        Implementation of search
        :param node: node
        :param num: desired number
        :return: Boolean True/False
        """
        if node.val == num:
            return True
        elif num < node.val and node.left != self.null_node:
            return self._find(node.left, num)
        elif num > node.val and node.right != self.null_node:
            return self._find(node.right, num)
        else:
            return False

    def inorder_print_tree(self):
        """
        Binary Tree inorder presentation
        :return: List of tree values
        """
        if self.root != self.null_node:
            return self._inorder_traversal(self.root, res=[])

    def _inorder_traversal(self, node, res=[]):
        """
        Implementation of inorder traversal printing
        :param node: node
        :return: List of tree values
        """
        if node is not self.null_node:
            self._inorder_traversal(node.left, res)
            res.append(node.val)
            self._inorder_traversal(node.right, res)
            return res

    def preorder_print_tree(self):
        """
        Binary Tree preorder presentation
        :return: List of tree values
        """
        if self.root != self.null_node:
            return self._preorder_traversal(self.root, res=[])

    def _preorder_traversal(self, node, res=[]):
        """
        Implementation of preorder traversal printing
        :param node: node
        :return: List of tree values
        """
        if node is not self.null_node:
            res.append(node.val)
            self._preorder_traversal(node.left, res)
            self._preorder_traversal(node.right, res)
            return res

    def postorder_print_tree(self):
        """
        Binary Tree postorder presentation
        :return: List of tree values
        """
        if self.root != self.null_node:
            return self._postorder_traversal(self.root, res=[])

    def _postorder_traversal(self, node, res=[]):
        """
        Implementation of postorder traversal printing
        :param node: node
        :return: List of tree values
        """
        if node is not self.null_node:
            self._postorder_traversal(node.left, res)
            self._postorder_traversal(node.right, res)
            res.append(node.val)
            return res

    def graphicalPrintTree(self):
        """
        Graphical Representation of Binary Tree
        :return: Graphs with format {parent: [child, child...]}
        """
        graph = collections.defaultdict(list)
        if self.root != self.null_node:
            stack = [self.root]
            # Graph generation into format {parent: [child, child...]}
            while stack:
                curr = stack.pop(0)
                for child in [curr.left, curr.right]:
                    if child != self.null_node:
                        if child.color == 0:
                            color = 'Black'
                        else:
                            color = 'Red'
                        graph[curr.val].append((child.val, color))
                        stack.append(child)
        return graph


def main():
    rb_test_tree = RedBlackBinaryTree()
    rb_test_tree.insert(55)
    rb_test_tree.insert(40)
    rb_test_tree.insert(30)
    rb_test_tree.insert(35)
    print(30 in rb_test_tree)
    print(50 in rb_test_tree)
    print("\nInorder Traversal: ")
    print(rb_test_tree.inorder_print_tree())
    print("\nPreorder Traversal: ")
    print(rb_test_tree.preorder_print_tree())
    print("\nPostorder Traversal: ")
    print(rb_test_tree.postorder_print_tree())
    print("\nGraphical Representation: ")
    print(rb_test_tree.graphicalPrintTree())


if __name__ == '__main__':
    main()



