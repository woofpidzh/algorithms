import random
import time
from statistics import mean
from numpy import average

counter = 0


# def counter(fu):
#     def inner(*a,**kw):
#         inner.count+=1
#         return fu(*a,**kw)
#     inner.count = 0
#     return inner

def create_array(N):
    arr = []
    arr[:] = ([random.uniform(-1, 1) for i in range(N)])
    return arr


# @counter
def q_sort(arr):
    global counter
    counter += 1
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = [i for i in arr[1:] if i <= pivot]

        right = [i for i in arr[1:] if i > pivot]

        return q_sort(left) + [pivot] + q_sort(right)


def calculations(N):
    for i in N:
        average = []

        for _ in range(20):
            arr = create_array(i)
            start = time.time()
            sorting = q_sort(arr)
            sorting_time = time.time() - start
            average.append(sorting_time)

        print(i, min(average), max(average), mean(average), counter)


def main():
    N = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]
    calculations(N)


if __name__ == '__main__':
    main()

