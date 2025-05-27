from StruttureDati.Node.NodeList import NodeList


class TreeNode(NodeList):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left, right)
        self.parent = parent
