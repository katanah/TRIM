from collections import deque
class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        
        
        
class Tree:
    def __init__(self, root: Node= None):
        self.root: Node = root
        self.children = deque()
    
    
        