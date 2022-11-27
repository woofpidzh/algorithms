import copy
from random import randint, choice
from time import perf_counter
import sys
sys.setrecursionlimit(500000000)

class Node:
  def __init__(self, key, degree):
    self.key = key
    self.children = []
    self.degree = degree


class BinomialTree:
  def __init__(self, root=None, initial_key=None):
    if root:
      self.root = root
    elif initial_key != None:
      self.root = Node(initial_key, 0)

  def union(self, tree):
    if tree.root.degree != self.root.degree:
      raise Exception("Can't union trees with different degrees")

    if self.root.key <= tree.root.key:
      self.root.children.append(tree.root)
      self.root.degree += 1
      return self

    tree.root.degree += 1
    tree.root.children.append(self.root)
    return tree
  
  def is_empty(self):
    return self.root == None

  def clear(self):
    self.root = None
  
  def size(self):
    return self.root.degree ** 2


class BinomialHeap:
  def __init__(self):
    self.trees = []
  
  def add_element(self, key):
    tree = BinomialTree(initial_key=key)
    self.trees.append(tree)
    self._fix_heap()
  
  def union(self, heap):
    self.trees.extend(heap.trees)
    self._fix_heap()
  
  def get_min_tree(self):
    if not len(self.trees):
      return None

    return min(self.trees, key = lambda tree: tree.root.key).root.key
  
  def remove_min(self):
    min_tree = min(self.trees, key = lambda tree: tree.root.key)
    if not min_tree:
      return

    self.trees.remove(min_tree)
    for root_child in min_tree.root.children:
      new_tree = BinomialTree(root=root_child)
      self.trees.append(new_tree)

    self._fix_heap() 
  
  def is_empty(self):
    return self.size() == 0
  
  def size(self):
    return len(self.trees)
  
  def clear(self):
    self.trees = []

  def _fix_heap(self):
    trees = self.trees
    trees.sort(key = lambda tree: tree.root.degree)
    was_merge = True

    while was_merge:
      was_merge = False
      for i in range(0, len(trees) - 1):
        if i >= len(self.trees) - 1:
          break
        
        if trees[i].root.degree == trees[i+1].root.degree:
          was_merge = True
          trees[i] = trees[i].union(trees[i+1])
          trees.pop(i+1)


class MinHeap(object):
    def __init__(self, heap):
        self.heap = copy.deepcopy(heap)
        if self.heap:
            self.heapify()

    def elements(self):
        return self.heap

    def length(self):
        return len(self.heap)

    def heapify(self):
        size = self.length()
        for index in reversed(range(size // 2)):
            self._heapify(index=index, size=size)

    def _heapify(self, index, size):
        l_index = self._left_child_index(index)
        r_index = self._right_child_index(index)
        largest_index = index
        if l_index < size and self.heap[l_index] < self.heap[index]:
            largest_index = l_index
        if r_index < size and self.heap[r_index] < self.heap[largest_index]:
            largest_index = r_index
        if largest_index != index:
            self.swap(largest_index, index)
            self._heapify(largest_index, size)

    def swim_up(self, index):
        self._swim_up(index=index)
        
    def _swim_up(self, index):
        if index == 1:
            return
        parent = (index // 2)
        if self.heap[parent - 1] < self.heap[index - 1]:
            return
        self.swap(parent - 1, index - 1)
        self._swim_up(index=parent)

    def get_root_value(self):
        return self.heap[0]

    def add_elementent(self, element):
        if isinstance(element, list):
            for _element in element:
                self.heap.append(_element)
                self.swim_up(self.length())
        else:
            self.heap.append(element)
            self.swim_up(self.length())

    def pop_root(self):
        self.swap(0, self.length() - 1)
        result = self.heap.pop()
        self._heapify(index=0, size=self.length())
        return result

    def search_value(self, value):
        size = self.length()
        for index in range(0, size):
            if self.heap[index] == value:
                return index
        return -1

    def swap(self, index1, index2):
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp

    def _left_child_index(self, index):
        return (2 * index) + 1

    def _right_child_index(self, index):
        return (2 * index) + 2


def list_generation(N):
    arr = [randint(0, 1000) for _ in range(N)]
    return arr
  
def main():
    f = open('results.txt', 'w+')
    for i in range(3, 8):
        print(i)
        N = 10 ** i
        f.write('\nNumber of list elements: ' + str(N))
        arr = list_generation(N)
        a = list_generation(1000)
      
        min_heap = MinHeap(arr)
        f.write('\nMinHeap: ')
        
        time_list = []
        start_time = perf_counter()
        for j in range(1000):
            st_time = perf_counter()
            min_heap.add_elementent(a[j])
            en_time = perf_counter()
            time_list.append(en_time - st_time)
            print(j)
        end_time = perf_counter()
        f.write('\nAdd time: ' + str((end_time - start_time)/1000))
        f.write('\nMax add time: ' + str(max(time_list)))
        
        time_list = []
        start_time = perf_counter()
        for _ in range(1000):
            st_time = perf_counter()
            min_heap.get_root_value()
            en_time = perf_counter()
            time_list.append(en_time - st_time)
        end_time = perf_counter()
        f.write('\nSearch time: ' + str((end_time - start_time)/1000))
        f.write('\nMax search time: ' + str(max(time_list)))

        time_list = []
        start_time = perf_counter()
        for j in range(1000):
            st_time = perf_counter()
            min_heap.pop_root()
            en_time = perf_counter()
            time_list.append(en_time - st_time)
        end_time = perf_counter()
        f.write('\nremove_min time: ' + str((end_time - start_time)/1000))
        f.write('\nMax remove_min time: ' + str(max(time_list)))
    
        binomial_heap = BinomialHeap()
        f.write('\nBinominalHeap: ')
        for x in arr:
            binomial_heap.add_element(x)

        time_list = []
        start_time = perf_counter()
        for j in range(1000):
            st_time = perf_counter()
            binomial_heap.add_element(a[j])
            en_time = perf_counter()
            time_list.append(en_time - st_time)
        end_time = perf_counter()
        f.write('\nAdd time: ' + str((end_time - start_time)/1000))
        f.write('\nMax add time: ' + str(max(time_list)))
        
        time_list = []
        start_time = perf_counter()
        for _ in range(1000):
            st_time = perf_counter()
            binomial_heap.get_min_tree()
            en_time = perf_counter()
            time_list.append(en_time - st_time)
        end_time = perf_counter()
        f.write('\nSearch time: ' + str((end_time - start_time)/1000))
        f.write('\nMax search time: ' + str(max(time_list)))

        time_list = []
        start_time = perf_counter()
        for _ in range(1000):
            st_time = perf_counter()
            binomial_heap.remove_min()
            en_time = perf_counter()
            time_list.append(en_time - st_time)
        end_time = perf_counter()
        f.write('\nremove_min time: ' + str((end_time - start_time)/1000))
        f.write('\nMax remove_min time: ' + str(max(time_list))) 

    f.close()

main()
