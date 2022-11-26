# lab3

from datetime import date
from random import randint
from numpy import sort
from platform import node
# from enum import Flag
# from operator import itemgetter


# from scipy import rand


class DoublyLinkedList:
    class Node:
        prev_node = None    # сохраняет ссылку на предыдущий узел
        element = None  # хранит фактические данные для узла
        next_node = None    # хранит ссылку на следующий узел

        def __init__(self, element, prev_node=None, next_node=None) -> None:
            self.prev_node = prev_node
            self.element = element
            self.next_node = next_node

        def __add__(self, n):
            return self.element + n

    length = 0
    head = 0
    tail = 0

    def add(self, element, index=None): # добавление
        self.length += 1
        if not self.head:
            self.head = self.Node(element)
            return element

        elif not self.tail:
            self.tail = self.Node(element, self.head, None)
            self.head.next_node = self.tail
            return element

        elif not index:
            self.tail = self.Node(element, self.tail, None)
            self.tail.prev_node.next_node = self.tail
            return element

        else:
            if index > self.length:
                raise Exception("Index error")
            node = self.head
            for i in range(index):
                node = node.next_node
            tmp = node
            node = self.Node(element, tmp.element, node.next_node)
            node.prev_node = tmp
            tmp.next_node = node
            return node

    def _del(self, index, reverse=False):
        if index == 0:
            el = self.head.element
            self.head = self.head.next_node
            self.head.prev_node = None
            return el

        elif index == self.length - 1:
            el = self.tail.element
            self.tail = self.tail.prev_node
            self.tail.next_node = None
            return el

        elif reverse:
            node = self.tail

            for i in range(self.length - 1, index, -1):
                node = node.prev_node

            el = node.element
            node.prev_node.next_node, node.next_node.prev_node = node.next_node, node.prev_node
            del node

            return el
        else:
            node = self.head

            for i in range(index):
                node = node.next_node

            el = node.element
            node.prev_node.next_node, node.next_node.prev_node = node.next_node, node.prev_node
            del node

            return el

    def delete(self, index):    # удаление
        if index > self.length:
            raise Exception("Index error")
        self.length -= 1

        if self.head:
            if index >= self.length // 2:
                el = self._del(index, reverse=True)
                return el
            elif index < self.length // 2:
                el = self._del(index, reverse=False)
                return el

    def is_empty(self): # проверка на пустоту
        return not self.length

    def sort(self): # сортировка
        node = self.head
        for i in range(self.length - 1):
            node2 = node
            for j in range(self.length - i - 1):
                if node2.element > node2.next_node.element:
                    node2.element, node2.next_node.element = node2.next_node.element, node2.element

                node2 = node2.next_node
            node = node.next_node

    def __iter__(self):
        node = self.head

        while node:
            yield node.element
            node = node.next_node

    def __ne__(self, __o: Node) -> bool:
        return __o.element


def analysis_1000():    # подсчет суммы, среднего, минимального и максимального
    DLlist = DoublyLinkedList()
    for i in range(1000):
        DLlist.add(randint(-1000, 1000))
    summ = 0
    min_value = DLlist.head.element
    max_value = DLlist.head.element
    for i in DLlist:
        summ += i
        if i < min_value:
            min_value = i
        if i > max_value:
            max_value = i
    avg_value = summ / DLlist.length
    print(f"min = {min_value} max = {max_value} avg = {avg_value}")


def analysis_str(): # проверка изъятия и вставка строк в список
    DLlist_str = DoublyLinkedList()
    for i in range(10):
        DLlist_str.add(f"str {i + 1}")
    for i in DLlist_str:
        print(i)
    print("Adding new element:")
    DLlist_str.add("New str", 4)
    for i in DLlist_str:
        print(i)
    print("Deleting an element (str 3):")
    DLlist_str.delete(2)
    for i in DLlist_str:
        print(i)


def analysis_struct():  # создание структуры из имен-фамилий-дат рождения и сортировка по возрасту
    DLlist_struct = DoublyLinkedList()
    for i in range(100):
        class Strct:
            firstname = f"firstname {i}"
            lastname = f"lastname {i}"
            otchestvo = f"otchestvo {i}"
            date_of_birth = date(randint(1980, 2020), randint(1, 12), randint(1, 28))

            def __str__(self):
                return self.date_of_birth

        DLlist_struct.add(Strct)

    DLlist_struct_new = DoublyLinkedList()
    for i in DLlist_struct:
        if i.date_of_birth < date(1990, 1, 1) or i.date_of_birth > date(2000, 1, 1):
            DLlist_struct_new.add(i)
    print("after sorting by birth date:")
    for i in DLlist_struct_new:
        print(i.date_of_birth)


def shake(DLlist: DoublyLinkedList):    # Перемешивание всех элементов в случайном порядке
    temp = DLlist.head
    for i in enumerate(DLlist):
        shake_index = randint(i[1] - 1, DLlist.length - 1)
        el = i[0]
        if shake_index == DLlist.length:
            el.element, DLlist.tail.element = DLlist.tail.element, el.element

        if shake_index == 0:
            continue

        node = DLlist.head
        for j in range(shake_index):
            node = node.next_node

        el, node.element = node.element, el


def main():
    # DLlist = DoublyLinkedList()

    # for i in tst:
    #     print(i)

    analysis_1000()
    analysis_str()

    analysis_struct()

    tst = DoublyLinkedList()
    for i in range(100):
        tst.add(randint(0, 100))

    #a = sorted(tst)
    tst.sort()
    for i in tst:
        print(i)
    print("shake:")
    shake(tst)
    for i in tst:
        print(i)


if __name__ == '__main__':
        main()