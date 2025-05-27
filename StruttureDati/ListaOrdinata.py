from StruttureDati.Node.NodeList import NodeList


class OrderedLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = NodeList(value)
        if self.head is None:
            self.head = new_node
            return

        if value < self.head.value:
            new_node.right = self.head
            self.head.left = new_node
            self.head = new_node
            return

            # Caso 3: inserimento nel mezzo o in coda
        current = self.head
        while current.right and current.right.value < value:
            current = current.right

        new_node.right = current.right
        new_node.left = current
        current.right = new_node
        if new_node.right:
            new_node.right.left = new_node

    def select(self, position):
        current = self.head
        index = 0
        while current:
            if index == position:
                return current.value
            current = current.right
            index += 1
        return None

    def rank(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.right
            index += 1
        return None

    def print(self):
        current = self.head
        print("Lista ordinata: ", end='')
        while current:
            print(current.value, end=' ')
            current = current.right
        print()
