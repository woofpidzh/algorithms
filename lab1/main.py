import random
from time import time
from statistics import mean  # Библиотека statistics содержит функцию mean() для определения среднего арифметического
import numpy as np


def array_creation(N):
    array = []
    array[:] = np.array([random.uniform(-1, 1) for i in range(N)])
    return array


def sorting(N):
    array = array_creation(N)
    left = 0
    right = N-1
    start_time = time()
    while left <= right:
        for i in range(left, right, +1):
            #print(array)
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
        right -= 1
        for i in range(right, left, -1):
            if array[i-1] > array[i]:
                array[i], array[i-1] = array[i-1], array[i]
        left += 1
    sort_time = time() - start_time
    return sort_time


def main():
    N = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]
    for i in N:
        average = []
        for j in range(20):
            result = sorting(i)
            average.append(result)
        print(i, min(average), max(average),
              mean(average))  # вывод лучшего, худшего и среднего затр. времени для каждого N


if __name__ == '__main__':
    main()
