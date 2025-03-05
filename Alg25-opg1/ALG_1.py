import time
from math import floor
from random import randint
from contextlib import contextmanager

# In this assignment, you will implement and test Insertion-Sort, Merge-Sort and
# Quicksort. First, you are given three utility functions, that are used for
# testing. Your task is to implement the insertion_sort, merge_sort and
# quicksort functions and their associated sub-procedures.


### UTILITY FUNCTIONS ###

@contextmanager
def performance():
    """A context manager that keeps track of time"""
    t1 = t2 = time.perf_counter()
    yield lambda: t2 - t1
    t2 = time.perf_counter()


def get_unsorted_lists(size, kind='random', n_copies=3):
    """
    Create two unsorted list of size `size` that is either completely random,
    almost sorted or reversed, depending on the `kind` argument
    """
    if kind == 'random':
        l = [randint(0, 10_000) for _ in range(size)]

    elif kind == 'almost_sorted':
        l = [randint(i - 2, i + 2) for i in range(size,)]

    elif kind == 'reversed':
        l = list(range(size, 0, -1))

    return [l.copy() for _ in range(n_copies)]


def is_sorted(A):
    """Checks if the list `A` is sorted"""
    return all(A[i] <= A[i+1] for i in range(len(A) - 1))


### YOUR IMPLEMENTATION GOES HERE ####

def binary_search(A, item, start, end):
    if start == end:
        return start if A[start] > item else start + 1
    if start > end:
        return start

    mid = (start + end) // 2
    if A[mid] < item:
        return binary_search(A, item, mid + 1, end)
    elif A[mid] > item:
        return binary_search(A, item, start, mid - 1)
    return mid

def insertion_sort(A, n):
    for i in range(1, n):
        key = A[i]
        j = i - 1
        loc = binary_search(A, key, 0, j)
        

        A[loc+1:i+1] = A[loc:i]
        A[loc] = key


def merge(A, p, q, r):

    leftA = A[p:q + 1]     
    rightA = A[q + 1:r + 1] 
    
    i, j, k = 0, 0, p
    

    while i < len(leftA) and j < len(rightA):
        if leftA[i] <= rightA[j]:
            A[k] = leftA[i]
            i += 1
        else:
            A[k] = rightA[j]
            j += 1
        k += 1
    

    while i < len(leftA):
        A[k] = leftA[i]
        i += 1
        k += 1
    

    while j < len(rightA):
        A[k] = rightA[j]
        j += 1
        k += 1


def merge_sort(A, p, r):
    if p < r:
        q = (p + r) // 2
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


def partition(A, p, r):
    pivot = randint(p,r)
    A[pivot],A[r] = A[r], A[pivot]
    x = A[r]
    i = p - 1

    for j in range(p, r):  
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    

    A[i + 1], x = x, A[i + 1]
    return i + 1

def quicksort(A, p, r):
    if p < r:
        pivotIndex = partition(A, p, r)
        quicksort(A, p, pivotIndex - 1)
        quicksort(A, pivotIndex + 1, r)  


if __name__ == '__main__':

    # different sizes of input to test on

    # different sizes of input to test on
    sizes = [1000, 10_000, 15_000, 25_000, 50_000, 100_000, 1_000_000]

    # keep track of much time each algorithm spends
    ms_max_time, is_max_time, qs_max_time = 0, 0, 0

    # set to 'random' to get a list of random number
    # set to 'reversed' to get a list in reversed sorted order
    # set to 'almost_sorted' to get an... almost sorted list
    kind = ['random','reversed','almost_sorted']  # experiment with changing this values
    with open("out.csv","w") as output:
        output.write("listtype,sorttype,size,time\n")
        for elm in kind:
            # main test loop
            ms_max_time, is_max_time, qs_max_time = 0, 0, 0
            for size in sizes:
                print(f"Test for size {size}")

                # since we are sorting in-place, we need 2 instances of the input list
                # (one for insertion sort and one for merge sort)
                l1, l2, l3 = get_unsorted_lists(size, kind=elm)
                
                # test Insertion-Sort, only if it took less than 5 seconds last time
                if is_max_time < 5:

                    # the 'with'-statement is just a helper to track time
                    with performance() as is_time:
                        insertion_sort(l1,len(l1))

                    # assert that the list godt sorted properly
                    assert is_sorted(l1), 'Oh oh, something wrong with insertion sort!'

                # test Merge-Sort, only if it took less than 5 seconds last time
                if ms_max_time < 5:

                    # the 'with'-statement is just a helper to track time
                    with performance() as ms_time:
                        merge_sort(l2,0,len(l2))

                    # assert that the list got sorted properly
                    assert is_sorted(l2), 'Oh oh, something wrong with merge sort!'

                # test QuickSort, only if it took less than 5 seconds last time
                if qs_max_time < 5:

                    # the 'with'-statement is just a helper to track time1)  # Changed to len(l3)-1
                    with performance() as qs_time:
                        quicksort((l3),0,len(l3)-1)

                    # assert that the list got sorted properly
                    assert is_sorted(l3), 'Oh oh, something wrong with quicksort!'
                
                output.write(f"{elm},Insertion,{size},{is_time()}\n")
                output.write(f"{elm},Merge,{size},{ms_time()}\n")
                output.write(f"{elm},Quick,{size},{qs_time()}\n")

                print(f'Insertion sort: {"-" if is_max_time > 5 else f"{is_time():0.4f}s"}')
                print(f'Merge sort: {"-" if ms_max_time > 5 else f"{ms_time():0.4f}s"}')
                print(f'Quicksort: {"-" if qs_max_time > 5 else f"{qs_time():0.4f}s"}')
                is_max_time = max(is_time(), is_max_time)
                qs_max_time = max(qs_time(), qs_max_time)
                ms_max_time = max(ms_time(), ms_max_time)
