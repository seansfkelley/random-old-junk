# Sean Kelley
# Comp 160, Fall 2010 -- Souvaine

# Written with Python 2.6.

# Constants to control randomized trials. A detailed description of how they're conducted is in the randomized_trials() function.

# How many randomized trials to perform for each tree type.
TRIALS = 10

# How many nodes are inserted during each trial.
NUM_NODES = 1000

# What percentage of nodes are deleted during each trial.
PCT_TO_DELETE = 0.2

# The percentage of elements that are out of place during insertions.
INSERTION_RANDOMNESS = 0.5

# Constants to control automated randomized trials, used for generating graphable data in a CSV format. Input values are modified
# along two dimensions -- how random the input is, and what percentage of the nodes are eventually deleted.

# The different values for what percentage of nodes will be deleted.
PCT_TO_DELETE_LIST = map(lambda x: x / 20.0, range(1, 20))

# The different values for how random the input data will be.
# Randomness == 0 is uninteresting, since the unbalanced tree devolves into a linked list which will obviously have dramatically
# inferior performance to the red-black tree.
INSERTION_RANDOMNESS_LIST = map(lambda x: x / 20.0, range(1, 21))

import random
import time
import math

# Other global constants.
DELETIONS = int(PCT_TO_DELETE * NUM_NODES)
RED, BLACK = True, False

class Node:
    parent = left = right = None
    color = None
    
    def __init__(self, value, color = None):
        "Instantiate a Node with the given value. If color is supplied, set it and set all the pointers to point to the sentinel node."
        self.value = value
        if color is not None:
            self.color = color
            self.parent = self.left = self.right = None_NODE
    
    def __nonzero__(self):
        "The sentinel node is the only node that evaluates to False."
        return self.value is not None
    


# The sentinel node with the special value None. It is the only node that should have the value None, and any others that do will
# cause undefined behavior in the tree. It is the only node that evaluates to False.
None_NODE = Node(None)
None_NODE.color = BLACK

class BinaryTree:
    root = None
    
    def __init__(self, values = None):
        """If values is supplied, construct an optimal binary tree. Otherwise, construct an empty tree."""
        if values:
            values = sorted(values)
            self.root = self._optimal_helper(values, 0, len(values) - 1)
    
    def _optimal_helper(self, values, left, right):
        """Recursively build an optimal BST using the supplied values."""
        if left > right:
            return None
        elif right == left:
            return Node(values[left])
        else:
            n = Node(values[(left + right) / 2])
            n.left = self._optimal_helper(values, left, (left + right) / 2 - 1)
            n.right = self._optimal_helper(values, (left + right) / 2 + 1, right)
            return n
    
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            parent = None
            current = self.root
            while current:
                parent = current
                if value < current.value:
                    current = current.left
                else:
                    current = current.right
            if value < parent.value:
                parent.left = Node(value)
            else:
                parent.right = Node(value)
    
    def delete(self, value):
        parent = None
        current = self.root
        while current and value != current.value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        self._delete_node(current, parent)
    
    def _delete_node(self, current, parent):
        """A helper function for delete that replaces a node with its in-order successor."""
        if current:
            if parent:
                if parent.left is current:
                    which = 'l'
                else:
                    which = 'r'
            else:
                which = None
            
            # If the node is a leaf, simply delete it.
            if not current.left and not current.right:
                if not which: self.root = None
                elif which is 'l': parent.left = None
                else: parent.right = None
                
            # If the node has two children, replace it with its in-order successor. This is most easily done by simply
            # copying the value (leaving the structure intact) and then calling this same function again to delete the
            # successor's original node, which we know has at most one child and will not trigger a second recursive call.
            elif current.left and current.right:
                replacement_parent = current
                replacement_current = current.right
                while replacement_current.left:
                    replacement_parent = replacement_current
                    replacement_current = replacement_current.left
                self._delete_node(replacement_current, replacement_parent)
                current.value = replacement_current.value
            
            # If the node only has one child, change the pointers to its parent points to
            # the child to delete this node.
            elif current.left:
                if not which: self.root = current.left
                elif which is 'l': parent.left = current.left
                else: parent.right = current.left
            
            # Symmetric to the previous case.
            else:
                if not which: self.root = current.right
                elif which is 'l': parent.left = current.right
                else: parent.right = current.right
    
    def find(self, value):
        """Returns the Node object containing the given value, or None if it doesn't exist."""
        current = self.root
        while current and value != current.value:
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return current
    
    def check_correctness(self, values):
        """Enforce that the tree contains exactly the given set of values, in sorted order."""
        if sorted(values) != self._inorder_values(self.root, []):
            raise Exception('Non-balacing BST nodes are not in sorted order.')
    
    def _inorder_values(self, root, values):
        """Get the node values in-order and append each one to the supplied list."""
        if not root:
            return values
        
        self._inorder_values(root.left, values)
        values.append(root.value)
        self._inorder_values(root.right, values)
        
        return values
    
    def preorder_print(self):
        self._preorder_print(self.root, 0)
    
    def _preorder_print(self, node, depth):
        if not node:
            # This will only happen if the parent of node had one child. Print 'nil' for consistency/spacing reasons
            # so we know which child is nil and which child has a value.
            print ' ' * depth + 'nil'
            return
        print ' ' * depth + str(node.value)
        if not node.left and not node.right:
            # If this is a leaf, don't print it (to avoid uninformative pairs of 'nil' lines).
            return
        self._preorder_print(node.left, depth + 1)
        self._preorder_print(node.right, depth + 1)
    


class RedBlackTree:
    root = None_NODE
    
    def insert(self, value):
        n = Node(value, RED)
        
        if not self.root:
            self.root = n
        else:
            parent = None
            current = self.root
            while current:
                parent = current
                if value < current.value:
                    current = current.left
                else:
                    current = current.right
            n.parent = parent
            if value < parent.value:
                parent.left = n
            else:
                parent.right = n
        
        self._insert_fixup(n)
    
    def _insert_fixup(self, fixup_node):
        # If we're the root, make it black and we're done.
        if fixup_node is self.root:
            fixup_node.color = BLACK
            return
        
        # No fixup required -- no invariants violated.
        if fixup_node.parent.color is BLACK:
            return
        
        # Parent and uncle are both red, so flip their colors and the color of the
        # grandparent. Since we made the grandparent red, we could have violated
        # invariants with it, so call this recursively.
        if fixup_node.parent.parent.left is fixup_node.parent:
            uncle = fixup_node.parent.parent.right
        else:
            uncle = fixup_node.parent.parent.left
        if uncle and uncle.color is RED:
            fixup_node.parent.color = uncle.color = BLACK
            fixup_node.parent.parent.color = RED
            self._insert_fixup(fixup_node.parent.parent)
            return
        
        # If the uncle is black, we begin by possibly rotating the subtree rooted at
        # fixup_node.parent outwards, if applicable.
        grandparent = fixup_node.parent.parent
        if fixup_node is fixup_node.parent.right and fixup_node.parent is grandparent.left:
            # Rotate the subtree towards the outside of the tree, leftwards.
            fixup_node = fixup_node.parent
            self._rotate_left(fixup_node)
        elif fixup_node is fixup_node.parent.left and fixup_node.parent is grandparent.right:
            # Rotate the subtree towards the outside of the tree, rightwards.
            fixup_node = fixup_node.parent
            self._rotate_right(fixup_node)
        # Don't return after this case -- it falls into the next one.
        
        # If the uncle is black, rotate fixup_node's parent upwards into its parent's position
        # and swap the colors of the affected nodes as appropriate.
        fixup_node.parent.color = BLACK
        fixup_node.parent.parent.color = RED
        if fixup_node is fixup_node.parent.left:
            # We are along the left side of the subtree.
            self._rotate_right(fixup_node.parent.parent)
        else:
            # We are along the right side of the subtree.
            self._rotate_left(fixup_node.parent.parent)
        
        # Done.
    
    def delete(self, value):
        n = self.find(value)
        
        if not n:
            return
        
        original_color = n.color
        if not n.left:
            # Handle one-child or no-child case.
            fixup_start = n.right
            self._replace_node(n, n.right) # Sets fixup_node.parent appropriately.
        elif not n.right:
            # Handle one-child case.
            fixup_start = n.left
            self._replace_node(n, n.left) # Sets fixup_node.parent appropriately.
        else:
            # Get the successor (and eventual replacement) to n and keep track of its original color.
            replacement = n.right
            while replacement.left:
                replacement = replacement.left
            original_color = replacement.color
            fixup_start = replacement.right
            
            if replacement.parent is n:
                # If we don't do a _replace_node, make sure fixup_node.parent is set appropriately.
                fixup_start.parent = replacement
            else:
                self._replace_node(replacement, replacement.right) # Sets fixup_node.parent appropriately.
                replacement.right = n.right
                replacement.right.parent = replacement
            
            # Do the actual replacement, deleting the node from the tree.
            self._replace_node(n, replacement)
            replacement.left = n.left
            replacement.left.parent = replacement
            replacement.color = n.color
        
        # We can only haev violated invariants if the node we eventually ended up deleting was black.
        if original_color is BLACK:
            self._delete_fixup(fixup_start)
    
    def _replace_node(self, dst, src):
        if not dst.parent:
            self.root = src
        elif dst is dst.parent.left :
            dst.parent.left = src
        else:
            dst.parent.right = src
        src.parent = dst.parent
    
    def _delete_fixup(self, fixup_node):
        while fixup_node is not self.root and fixup_node.color is BLACK:
            if fixup_node is fixup_node.parent.left:
                sibling = fixup_node.parent.right
                
                # Case 1: The sibling is red. We want it to be black and we don't yet care about the color
                # of anything else. Make it black. Since it was red, it had two black children, so the new
                # sibling of fixup_node must be black and we have converted to some other case without
                # violating any further invariants.
                if sibling.color is RED:
                    sibling.color = BLACK
                    fixup_node.parent.color = RED
                    self._rotate_left(fixup_node.parent)
                    sibling = fixup_node.parent.right
                
                # Case 2: The sibling has two black children. Demote fixup_node to be singly black (no actual 
                # property change required) and demote the sibling to be red. Start the loop over again with
                # a new fixup_node -- for which we only need to keep doing work if we're still working with a
                # black node and therefore have not fixed the double-black problem.
                if sibling.left.color is BLACK and sibling.right.color is BLACK:
                    sibling.color = RED
                    # This can be converted into a recursive method like _insert_fixup() by calling it here and
                    # properly inserting return statements to terminate in the right places. This is the only time
                    # that the node is reassigned and the loop is repeated.
                    fixup_node = fixup_node.parent
                else:
                    # Case 3: We want to convert to case four, but the sibling's right child is black. Perform
                    # recolorings and rotations as appropriate (and avoiding violating any more invariants)
                    # in order to achieve this. We know the left sibling is red because if it was black, and the
                    # right sibling is black, it would hav been case 2. Fall into case 4 afterwards.
                    if sibling.right.color is BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._rotate_right(sibling)
                        sibling = fixup_node.parent.right
                    
                    # Case 4: Remove the extra black on fixup_node by rearranging the colors and performing a
                    # rotation. We know this fixes the problem for the whole tree, so we set the root as the 
                    # next node to be examined so the algorithm terminates.
                    sibling.color = fixup_node.parent.color
                    fixup_node.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._rotate_left(fixup_node.parent)
                    fixup_node = self.root
            else:
                # Symmetric to the if block.
                sibling = fixup_node.parent.left
                if sibling.color is RED:
                    sibling.color = BLACK
                    fixup_node.parent.color = RED
                    self._rotate_right(fixup_node.parent)
                    sibling = fixup_node.parent.left
                
                if sibling.left.color is BLACK and sibling.right.color is BLACK:
                    sibling.color = RED
                    fixup_node = fixup_node.parent
                else:
                    if sibling.left.color is BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._rotate_left(sibling)
                        sibling = fixup_node.parent.left
                    
                    sibling.color = fixup_node.parent.color
                    fixup_node.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._rotate_right(fixup_node.parent)
                    fixup_node = self.root
        
        fixup_node.color = BLACK
    
    def find(self, value):
        """Return the Node object containing the given value, or the sentinel node if it doesn't exist."""
        current = self.root
        while current and value != current.value:
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return current
    
    def _rotate_left(self, rotate_root):
        if not rotate_root.right:
            raise Exception('Can\'t rotate left -- no right child of root.')
        
        new_root = rotate_root.right
        
        # Swap inner subtree between roots.
        rotate_root.right = new_root.left
        if new_root.left:
            new_root.left.parent = rotate_root
        
        # Change which root the parent of this subtree points to.
        new_root.parent = rotate_root.parent
        if not rotate_root.parent:
            self.root = new_root
        elif rotate_root.parent.left is rotate_root:
            rotate_root.parent.left = new_root
        else:
            rotate_root.parent.right = new_root
        
        # Make old root a child of the new root.
        new_root.left = rotate_root
        rotate_root.parent = new_root
    
    def _rotate_right(self, rotate_root):
        if not rotate_root.left:
            raise Exception('Can\'t rotate right -- no left child of root.')
        
        new_root = rotate_root.left
        
        rotate_root.left = new_root.right
        if new_root.right:
            new_root.right.parent = rotate_root
        
        new_root.parent = rotate_root.parent
        if not rotate_root.parent:
            self.root = new_root
        elif rotate_root.parent.right is rotate_root:
            rotate_root.parent.right = new_root
        else:
            rotate_root.parent.left = new_root
            
        new_root.right = rotate_root
        rotate_root.parent = new_root
    
    def check_correctness(self, values):
        """Enforce that the tree contains exactly the given set of values, in sorted order, and check structural invariants."""
        if not self.root:
            return True
        
        if self.root.color is RED:
            raise Exception('Red-black tree root is red.')
        
        self._recursive_invariant_check(self.root)
        
        if sorted(values) != self._inorder_values(self.root, []):
            raise Exception('Red-black tree nodes are not in sorted order.')
    
    def _recursive_invariant_check(self, node):
        """Descend the tree, checking that black heights are correct and that there are no two red nodes in a row.
        Return the black height of the given node, INCLUDING the node itself.
        """
        if not node:
            # Base case -- including themselves, the leaf nodes have a black height of one.
            return 1
        
        if node.color is RED and (node.left.color is RED or node.right.color is RED):
            raise Exception('Red-black tree red node has a red child.')
        
        left_black_height, right_black_height = self._recursive_invariant_check(node.left), self._recursive_invariant_check(node.right)
        
        if left_black_height != right_black_height:
            raise Exception('Red-black tree black heights are not the same.')
        
        # Increase the black height of this subtree, if appropriate.
        if node.color is BLACK:
            left_black_height += 1
        return left_black_height
    
    def _inorder_values(self, root, values):
        if not root:
            return values
        
        self._inorder_values(root.left, values)
        values.append(root.value)
        self._inorder_values(root.right, values)
        
        return values
    
    def preorder_print(self):
        self._preorder_print(self.root, 0)
    
    def _preorder_print(self, node, depth):
        if not node:
            print ' ' * depth + 'nil'
            return
        print ' ' * depth + str(node.value),
        if node.color is BLACK:
            print 'B'
        else:
            print 'R'
        if not node.left and not node.right:
            return
        if node.left and node.left.parent is not node:
            raise Exception('Left child\'s parent is not self.')
        if node.right and node.right.parent is not node:
            raise Exception('Right child\'s parent is not self.')
        self._preorder_print(node.left, depth + 1)
        self._preorder_print(node.right, depth + 1)
    


def insert_values_permutation(insert_values, randomness = INSERTION_RANDOMNESS):
    """Permute the given values by sorting them, then taking a percentage to shuffle and reinsert in random positions."""
    split_index = int(randomness * len(insert_values))
    random.shuffle(insert_values)
    sorted_elements = sorted(insert_values[split_index:])
    random_elements = insert_values[:split_index]
    
    while random_elements:
        sorted_elements.insert(random.randint(0, len(insert_values)), random_elements.pop())
    
    return sorted_elements


def randomized_trials():
    """Conduct one set of randomized trials for a fixed deletion percentage and randomness factor as defined by the global variables.
    For each tree, the following is performed during each trial: insert all the values in the order produced by the random factor and
    insert_values_permutation(). Then delete a percentage of these values, at random (the same randomly-selected set for each tree).
    Lastly, do a find on all values that were ever inserted (whether they are deleted or not). After all insertions/deletions, check
    the correctness of each tree against what values should be in it. After all trials have finished, average the times spent for each
    operation.
    """
    print 'Testing non-balancing BST, optimal BST, and red-black trees with %d trials:\n%d insertions (%d%% random)\n%d deletions\n%d finds' % \
        (TRIALS, NUM_NODES, 100 * INSERTION_RANDOMNESS, DELETIONS, NUM_NODES)
    binary_insert = binary_delete = binary_find = 0
    rb_insert = rb_delete = rb_find = 0
    optimal_find = 0
    
    for trial in xrange(TRIALS):
        insert_values = insert_values_permutation(range(NUM_NODES))
        delete_values = random.sample(insert_values, DELETIONS)
        remaining_values = list(set(insert_values) - set(delete_values))
        
        tree = BinaryTree()
        
        t_start = time.time()
        for v in insert_values:
            tree.insert(v)
        t_inserted = time.time()
        for v in delete_values:
            tree.delete(v)
        t_deleted = time.time()
        for v in insert_values:
            tree.find(v)
        t_found = time.time()
        
        tree.check_correctness(remaining_values)
        
        binary_insert += t_inserted - t_start
        binary_delete += t_deleted - t_inserted
        binary_find += t_found - t_deleted
        
        tree = RedBlackTree()
        
        t_start = time.time()
        for v in insert_values:
            tree.insert(v)
        t_inserted = time.time()
        for v in delete_values:
            tree.delete(v)
        t_deleted = time.time()
        for v in insert_values:
            tree.find(v)
        t_found = time.time()
        
        tree.check_correctness(remaining_values)
        
        rb_insert += t_inserted - t_start
        rb_delete += t_deleted - t_inserted
        rb_find += t_found - t_deleted
        
        tree = BinaryTree(remaining_values)
        tree.check_correctness(remaining_values)
        
        t_start = time.time()
        for v in insert_values:
            tree.find(v)
        t_found = time.time()
        
        optimal_find += t_found - t_start
    
    print 'Non-Balancing BST'
    print 'insertion: %7.2f seconds = %7.2f usec/node' % (binary_insert, 1000000 * binary_insert / TRIALS / NUM_NODES)
    print 'deletion:  %7.2f seconds = %7.2f usec/node' % (binary_delete, 1000000 * binary_delete / TRIALS / DELETIONS)
    print 'find:      %7.2f seconds = %7.2f usec/node' % (binary_find,   1000000 * binary_find / TRIALS / NUM_NODES)
    print
    
    print 'Optimal BST'
    print 'find:      %7.2f seconds = %7.2f usec/node' % (optimal_find, 1000000 * optimal_find / TRIALS / NUM_NODES)
    print
    
    print 'Red-Black Tree'
    print 'insertion: %7.2f seconds = %7.2f usec/node' % (rb_insert, 1000000 * rb_insert / TRIALS / NUM_NODES)
    print 'deletion:  %7.2f seconds = %7.2f usec/node' % (rb_delete, 1000000 * rb_delete / TRIALS / DELETIONS)
    print 'find:      %7.2f seconds = %7.2f usec/node' % (rb_find,   1000000 * rb_find / TRIALS / NUM_NODES)


def generate_graph_data():
    """Performs the same tests as randomized_trials(), except with varying randomnesses and deletion percentages and without
    checking correctness of the trees each and every time. Prints out in CSV format, in the following order:
    randomness, deletion percentage, bst insert avg, bst delete avg, bst find avg, optimal find avg, rb insert avg, rb delete avg, rb find avg
    where 'avg' refers to the per-node average execution time of the action, in microseconds.
    """
    for randomness in INSERTION_RANDOMNESS_LIST:
        for delete_pct in PCT_TO_DELETE_LIST:
            binary_insert = binary_delete = binary_find = 0
            rb_insert = rb_delete = rb_find = 0
            optimal_find = 0
    
            for trial in xrange(TRIALS):
                insert_values = insert_values_permutation(range(NUM_NODES), randomness)
                delete_values = random.sample(insert_values, int(NUM_NODES * delete_pct))
                remaining_values = list(set(insert_values) - set(delete_values))
        
                tree = BinaryTree()
        
                t_start = time.time()
                for v in insert_values:
                    tree.insert(v)
                t_inserted = time.time()
                for v in delete_values:
                    tree.delete(v)
                t_deleted = time.time()
                for v in insert_values:
                    tree.find(v)
                t_found = time.time()
        
                binary_insert += t_inserted - t_start
                binary_delete += t_deleted - t_inserted
                binary_find += t_found - t_deleted
        
                tree = RedBlackTree()
        
                t_start = time.time()
                for v in insert_values:
                    tree.insert(v)
                t_inserted = time.time()
                for v in delete_values:
                    tree.delete(v)
                t_deleted = time.time()
                for v in insert_values:
                    tree.find(v)
                t_found = time.time()
        
                rb_insert += t_inserted - t_start
                rb_delete += t_deleted - t_inserted
                rb_find += t_found - t_deleted
        
                tree = BinaryTree(remaining_values)
        
                t_start = time.time()
                for v in insert_values:
                    tree.find(v)
                t_found = time.time()
        
                optimal_find += t_found - t_start
    
            print '%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f' % \
                (randomness, delete_pct,
                1000000 * binary_insert / TRIALS / NUM_NODES,
                1000000 * binary_delete / TRIALS / int(NUM_NODES * delete_pct),
                1000000 * binary_find / TRIALS / NUM_NODES,
                1000000 * optimal_find / TRIALS / NUM_NODES,
                1000000 * rb_insert / TRIALS / NUM_NODES,
                1000000 * rb_delete / TRIALS / int(NUM_NODES * delete_pct),
                1000000 * rb_find / TRIALS / NUM_NODES)
    


if __name__ == '__main__':
    generate_graph_data()
    # randomized_trials()