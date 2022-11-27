from random import randint, choice
from time import perf_counter
import sys
sys.setrecursionlimit(500000000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1


class Rand_tree:
    def getsize(self, node):
        if node is None:
            return 0
        return node.size

    def fixsize(self, node):
        node.size = self.getsize(node.left) + self.getsize(node.right) + 1
    
    def find(self, node, val):
        if node is None:
            return node
        if val == node.value:
            return node
        if val < node.value:
            return self.find(node.left, val)
        if val > node.value:
            return self.find(node.right, val)

    def rotateR(self, node):
        q = node.left
        if q is None:
            return node
        node.left = q.right
        q.right = node
        q.size = node.size
        self.fixsize(node)
        self.fixheight(node)
        self.fixheight(q)
        return q

    def rotateL(self, node):
        p = node.right
        if p is None:
            return node
        node.right = p.left
        p.left = node
        p.size = node.size
        self.fixsize(node)
        self.fixheight(node)
        self.fixheight(p)
        return p

    def insertroot(self, node, val):
        if node is None:
            return Node(val)
        if val < node.value:
            node.left = self.insertroot(node.left, val)
            return self.rotateR(node)
        else:
            node.right = self.insertroot(node.right, val)
            return self.rotateL(node)

    def insert(self, node, val):
        if node is None:
            return Node(val)
        if randint(0, node.size) == 0:
            return self.insertroot(node, val)
        if node.value > val:
            node.left = self.insert(node.left, val)
        else:
            node.right = self.insert(node.right, val)
        self.fixsize(node)
        return node
    
    def join(self, p, q):
        if p is None:
            return q
        if q is None:
            return p
        if randint(0, p.size + q.size - 1) < p.size:
            p.right = self.join(p.right, q)
            self.fixsize(p)
            return p
        else:
            q.left = self.join(p, q.left)
            self.fixsize(q)
            return q

    
    def remove(self, node, val):
        if node is None:
            return node
        if val < node.value:
            node.left = self.remove(node.left, val)
        elif val > node.value:
            node.right = self.remove(node.right, val)
        else:
            q = self.join(node.left, node.right)
            node = None
            return q   
        return node

    def height(self, node):
        return node.height if node else 0
    
    def fixheight(self, node):
        hl = self.height(node.left)
        hr = self.height(node.right)
        if hl > hr:
            node.height = hl + 1
        else:
            node.height = hr + 1
        return node.height

    def find_leafs(self, node):
        global leafs
        self.find_leafs_(node)
        return sum(leafs)/len(leafs)
            
    def find_leafs_(self, node):
        global leafs
        if node is None:
            return node
        if node.left is not None:
            node.left.height = node.height + 1
            self.find_leafs_(node.left)
        if node.right is not None:
            node.right.height = node.height + 1
            self.find_leafs_(node.right)
        if node.left is None and node.right is None:
            leafs.append(node.height)
    

class AVL:
    def height(self, node):
        return node.height if node else 0

    def bfactor(self, node):
        return self.height(node.right) - self.height(node.left)

    def fixheight(self, node):
        hl = self.height(node.left)
        hr = self.height(node.right)
        if hl > hr:
            node.height = hl + 1
        else:
            node.height = hr + 1
        return node.height
        
    def rotateR(self, node):
        q = node.left
        node.left = q.right
        q.right = node
        self.fixheight(node)
        self.fixheight(q)
        return q

    def rotateL(self, node):
        p = node.right
        node.right = p.left
        p.left = node
        self.fixheight(node)
        self.fixheight(p)
        return p

    def balance(self, node):
        self.fixheight(node)
        if self.bfactor(node) == 2:
            if self.bfactor(node.right) < 0:
                node.right = self.rotateR(node.right)
            return self.rotateL(node)
        if self.bfactor(node) == -2:
            if self.bfactor(node.left) > 0:
                node.left = self.rotateL(node.left)
            return self.rotateR(node)
        return node
    
    def insert(self, node, val):
        if node is None:
            return Node(val)
        if val < node.value:
            node.left = self.insert(node.left, val)
        else:
            node.right = self.insert(node.right, val)
        return self.balance(node)

    def findmin(self, node):
        return self.findmin(node.left) if node.left else node

    def removemin(self, node):
        if node.left is None:
            return node.right
        node.left = self.removemin(node.left)
        return self.balance(node)

    def remove(self, node, val):
        if node is None:
            return node
        if val < node.value:
            node.left = self.remove(node.left, val)
        elif val > node.value:
            node.right = self.remove(node.right, val)
        else:
            q = node.left
            r = node.right
            p = None
            if r is None:
                return q
            minimum = self.findmin(r)
            minimum.right = self.removemin(r)
            minimum.left = q
            return self.balance(minimum)
        return self.balance(node)

    def find(self, node, val):
        if node is None:
            return node
        elif val < node.value:
            node.left = self.find(node.left, val)
        elif val > node.value:
            node.right = self.find(node.right, val)
        else:
            return node
        


def list_generation(N):
    arr = [randint(0, 1000) for _ in range(N)]
    return arr  


if __name__ == "__main__":
    rand_tree = Rand_tree()
    AVL_tree = AVL()
    
    f = open('resultsnew.txt', 'w+')
    global leafs
    for i in range(10, 19):
        n = 2 ** i
        time_ins, time_find, time_rem, fix, len_leafs = 0, 0, 0, 0, 0
        time_ins_avl, time_find_avl, time_rem_avl, fix_avl = 0, 0, 0, 0
        f.write('\nNumber of list elements: ' + str(n))
        print(i)
        for j in range(50):
            arr = list_generation(n)
            root = None
            for k in arr:
                root = rand_tree.insert(root, k)
            fix += rand_tree.fixheight(root)
            leafs = []
            root.height = 0
            len_leafs += rand_tree.find_leafs(root)
            
            arr_y = [randint(0, 1000) for _ in range(1000)]
            start_time = perf_counter()
            for k in arr_y:
                root = rand_tree.insert(root, k)
            stop_time = perf_counter()
            time_ins += stop_time - start_time

            start_time = perf_counter()
            for _ in range(1000):
                num = choice(arr)
                root = rand_tree.find(root, num)
            stop_time = perf_counter()
            time_find += stop_time - start_time

            start_time = perf_counter()
            for k in range(1000):
                num = choice(arr)
                root = rand_tree.remove(root, num)
            stop_time = perf_counter()
            time_rem += stop_time - start_time


            root = None
            for k in arr:
                root = AVL_tree.insert(root, k)
            fix_avl += AVL_tree.fixheight(root)
            
            start_time = perf_counter()
            for k in arr_y:
                root = AVL_tree.insert(root, k)
            stop_time = perf_counter()
            time_ins_avl += stop_time - start_time

            start_time = perf_counter()
            for _ in range(1000):
                num = choice(arr)
                root = AVL_tree.find(root, num)
            stop_time = perf_counter()
            time_find_avl += stop_time - start_time

            start_time = perf_counter()
            for k in range(1000):
                num = choice(arr)
                root = AVL_tree.remove(root, num)
            stop_time = perf_counter()
            time_rem_avl += stop_time - start_time

        f.write('\n####################  Rand_tree  ####################')
        f.write('\nInsertion time: ' + str(time_ins / 50))
        f.write('\nSearch time: ' + str(time_find / 50))
        f.write('\nRemoval time: ' + str(time_rem / 50))
        f.write('\nHeight tree: ' + str(fix / 50))
        f.write('\nlen leafs: ' + str(len_leafs / 50))
        f.write('\n####################  AVL_tree  ####################')
        f.write('\nInsertion time: ' + str(time_ins_avl / 50))
        f.write('\nSearch time: ' + str(time_find_avl / 50))
        f.write('\nRemoval time: ' + str(time_rem_avl / 50))
        f.write('\nHeight tree: ' + str(fix_avl / 50))
    f.close()

