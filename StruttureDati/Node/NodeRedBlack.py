from StruttureDati.Node.TreeNode import TreeNode


class NodeRedBlack(TreeNode):
    def __init__(self, value=None, color='Black', left=None, right=None, parent=None, size=1):
        super().__init__(value, left, right, parent)
        self.color = color
        self.size = size
