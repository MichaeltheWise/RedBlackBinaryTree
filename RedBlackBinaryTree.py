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

    # def __contains__(self, key):
    #     return self.find(key)

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

        self.rebalance(new_node)

    def rebalance(self, node):
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

    def inorder_print_tree(self):
        """
        Binary Tree in order presentation
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
    print(rb_test_tree.graphicalPrintTree())


if __name__ == '__main__':
    main()



