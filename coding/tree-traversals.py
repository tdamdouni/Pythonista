# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

def preorder(root):
    if root is not None:
        print(root.data)
        preorder(root.left)
        preorder(root.right)

def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root.data)
        inorder(root.right)

def postorder(root):
    if root is not None:
        postorder(left)
        postorder(right)
        print(root.data)
