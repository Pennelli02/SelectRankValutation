from StruttureDati.Node.NodeRedBlack import NodeRedBlack


class TreeRedBlack:
    def __init__(self):
        self.Nil = NodeRedBlack(color='Black', size=0)
        self.Nil.left = self.Nil.right = self.Nil.parent = self.Nil
        self.root = self.Nil

    def insert(self, value):
        z = NodeRedBlack(value=value, color='Red', left=self.Nil, right=self.Nil, parent=self.Nil, size=1)
        y = self.Nil
        x = self.root

        while x != self.Nil:
            x.size += 1  # Incrementa size per ogni nodo attraversato
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.Nil:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z

        self.rb_Insert_Fixup(z)

    def rb_Insert_Fixup(self, z):
        while z.parent.color == 'Red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # zio
                if y.color == 'Red':  # Caso 1
                    z.parent.color = 'Black'
                    y.color = 'Black'
                    z.parent.parent.color = 'Red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:  # Caso 2
                        z = z.parent
                        self.left_Rotate(z)
                    z.parent.color = 'Black'  # Caso 3
                    z.parent.parent.color = 'Red'
                    self.right_Rotate(z.parent.parent)
            else:
                y = z.parent.parent.left  # zio
                if y.color == 'Red':  # Caso 1
                    z.parent.color = 'Black'
                    y.color = 'Black'
                    z.parent.parent.color = 'Red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:  # Caso 2
                        z = z.parent
                        self.right_Rotate(z)
                    z.parent.color = 'Black'  # Caso 3
                    z.parent.parent.color = 'Red'
                    self.left_Rotate(z.parent.parent)

        self.root.color = 'Black'

    def left_Rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.Nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == self.Nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

        # Aggiorna size
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def right_Rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.Nil:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == self.Nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

        # Aggiorna size
        x.size = y.size
        y.size = y.left.size + y.right.size + 1

    def Os_Select(self, node, i):
        if node == self.Nil:
            return None

        rank = node.left.size + 1
        if i == rank:
            return node.value
        elif i < rank:
            return self.Os_Select(node.left, i)
        else:
            return self.Os_Select(node.right, i - rank)

    def Os_Rank(self, node):
        if node == self.Nil:
            return 0

        rank = node.left.size + 1
        while node != self.root:
            if node == node.parent.right:
                rank += node.parent.left.size + 1
            node = node.parent
        return rank

    def inorder(self, node):
        if node != self.Nil:
            self.inorder(node.left)
            print(f"{node.value} Size: {node.size}")
            self.inorder(node.right)

    def search(self, value):
        node = self.root
        while node != self.Nil:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return None
