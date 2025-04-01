import re
import glob
from models import BinarySearchTree
from utils import parse_date_str, parse_datetime, get_most_frequent


def get_task_files(task_path):
    """
    Returns a list of (data_file, solution_file) tuples for the task specified
    by `task_path', sorted by number of elements in the task (not pretty)
    """
    fs = glob.glob(task_path + '*')
    tasks, solutions = [], []
    for file in fs:
        if 'solution' in file:
            solutions.append(file)
        else:
            tasks.append(file)

    tasks.sort(key=lambda x: int(re.search('_(\d+)', x).group(1)))
    solutions.sort(key=lambda x: int(re.search('_(\d+)', x).group(1)))

    return [(tasks[i], solutions[i]) for i in range(len(tasks))]


def test_task1():
    files = get_task_files('./data/task1')

    # run through the files
    for data, solution in files:
        print(f'run with {data}')

        # here we instatiate your tree
        tree = BinarySearchTree()

        # read the data file
        with open(data, 'r') as f:
            n = int(f.readline())
            for _ in range(n):
                # read a line
                line = f.readline()

                # get name and date of birth
                name, dob = line.strip('\n').split(' ')

                # this inserts key/value pairs into the tree
                tree.insert(parse_datetime(dob), name)

            # read a line and parse strings as datetime objects
            line = f.readline().strip('\n')
            start, end = map(parse_datetime, line.split(' - '))

        # here we call your functions
        query = tree.range(start, end)
        name, count = get_most_frequent(query)

        # read solution
        with open(solution, 'r') as f:
            correct_name, correct_count = f.readline().strip('\n').split(' ')

        # assert that your functions returned the correct things
        assert correct_name == name, f'wrong name in {data}'
        assert int(correct_count) == count, f'wrong count in {data}'

    print('Task 1 solved correctly!')


def test_task2():
    files = get_task_files('./data/task2')

    for data, solution in files:
        print(f'run with {data}')

        # instatiate your tree
        tree = BinarySearchTree()

        # read the data files
        with open(data, 'r') as f:
            n = int(f.readline())

            # insert all the elements into the tree
            for i in range(n):
                name, dob = f.readline().strip('\n').split(' ')
                tree.insert(parse_datetime(dob), name)

            # get the rank we are searching for
            rank = int(f.readline())

        # call your method
        x = tree.select(rank)

        # read solution
        with open(solution, 'r') as f:
            name, dob = f.readline().strip('\n').split(' ')

        # compare your output with the correct
        assert name == x.value, f'wrong name in {data}'
        assert dob == parse_date_str(x.key), f'wrong dob in {data}'

    print('Task 2 solved successfully!')


if __name__ == '__main__':
    test_task1()

    print()

    test_task2()
