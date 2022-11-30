from random import randint
import json

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def validation_error(msg):

    return [{"non_field_errors":msg}]