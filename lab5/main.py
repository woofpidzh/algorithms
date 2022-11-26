# lab 5
from random import randint
import numpy as np
import time


class Graph:
    nodes = []
    links = []
    weight = []
    count = 0
    adj_matrix = []

    def __init__(self, nodes, links, weight):
        self.nodes = nodes
        self.links = links
        self.weight = weight
        self.count = len(nodes)
        self.adj_matrix = np.zeros((self.count, self.count))
        self.create_adjacency_matrix()

    def create_adjacency_matrix(self):
        for i in range(len(self.links)):
            j = self.links[i]
            self.adj_matrix[j[0], j[1]] = self.weight[i]
            self.adj_matrix[j[1], j[0]] = self.weight[i]

    def print_links(self):
        print(self.links)

    def print_adjacency_matrix(self):
        print(self.adj_matrix)

    def print_adjacency_list(self):
        print(self.adj_list)

    def prim(self):
        start = time.time()
        tree = []
        visited = []
        visited.append(randint(0, self.count - 1))
        canVisit = []
        while visited != self.nodes:
            for cur in visited:
                for i in range(len(self.adj_matrix[cur])):
                    if self.adj_matrix[cur][i] > 0 and not (i in visited) and not (i in canVisit):
                        canVisit.append(i)
            min = 21
            for cur in canVisit:
                for i in range(len(self.adj_matrix[cur])):
                    if self.adj_matrix[cur][i] > 0 and not (i in visited):
                        if min > self.adj_matrix[cur][i]:
                            min = self.adj_matrix[cur][i]
                            minIndex = (cur, i)
            visited.append(minIndex[1])
            visited.sort()
            tree.append((minIndex, self.adj_matrix[minIndex[0]][minIndex[1]]))
        sum = 0
        for i in tree:
            sum += i[1]
        print(sum)
        print(tree)
        return time.time() - start


def generate_graph(nodeQuantity, edgesPerNode):
    nodes = []
    links = []
    weight = []
    for i in range(nodeQuantity):
        nodes.append(i)
    for j in range(edgesPerNode):
        for i in range(len(nodes)):
            links.append((nodes[i], nodes[randint(0, len(nodes) - 1)]))
            weight.append((randint(1, 20)))
    visited = []
    while visited != nodes:
        toVisit = []
        visited = []
        toVisit.append(randint(0, len(nodes) - 1))
        while len(toVisit) > 0:
            current = toVisit.pop()
            visited.append(current)
            for i in links:
                if i[0] == current:
                    if not ((i[1] in visited) or (i[1] in toVisit)):
                        toVisit.append(i[1])
                elif i[1] == current:
                    if not ((i[0] in visited) or (i[0] in toVisit)):
                        toVisit.append(i[0])
        visited.sort()
        for i in nodes:
            if not (i in visited):
                links.append((i, visited[randint(0, len(visited) - 1)]))
                weight.append((randint(1, 20)))
    return [nodes, links, weight]


def main():
    nodes_arr = [10, 20, 50, 100]
    edges_arr = [3, 4, 10, 20]
    for i in range(len(nodes_arr)):
        ans_arr = []
        gen = generate_graph(nodes_arr[i], edges_arr[i])
        mygraph = Graph(gen[0], gen[1], gen[2])
        for j in range(5):
            ans_arr.append(mygraph.prim())
        print('nodes: {}, edges: {}, time: {}'.format(nodes_arr[i], edges_arr[i], sum(ans_arr) / len(ans_arr)))


if __name__ == '__main__':
    main()