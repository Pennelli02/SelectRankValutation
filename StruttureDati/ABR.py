from StruttureDati.Node.TreeNode import TreeNode


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        z = TreeNode(value)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z

    def os_select(self, position):
        stack = []
        current = self.root
        count = 0

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            count += 1
            if count == position:
                return current.value  # ritorni il valore del nodo
            current = current.right

        return None  # se position > numero nodi

    def os_rank(self, value):
        stack = []
        current = self.root
        rank = 0

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            rank += 1
            if current.value == value:
                return rank
            current = current.right

        return 0  # se non trovato

    def print(self, root):
        if root is None:
            return
        self.print(root.left)
        print(root.value)
        self.print(root.right)

