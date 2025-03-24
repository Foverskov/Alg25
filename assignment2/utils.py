from collections import defaultdict
from datetime import datetime


def get_most_frequent(arr):
    """
    This function takes as input a list of nodes and returns the most frequent
    value associated with these nodes as well as the number of times that value
    occurs.
    """
    count = defaultdict(int)
    popular = None
    for x in arr:
        count[x.value] += 1
        if count[x.value] > count[popular]:
            popular = x.value
    return popular, count[popular]


def parse_datetime(time_str, fstr='%d/%m/%Y'):
    """Creates a `datetime` object from a string"""
    return datetime.strptime(time_str, fstr)


def parse_date_str(dt, fstr='%d/%m/%Y'):
    """Format a `datetime` object as a string"""
    return dt.strftime(fstr)
