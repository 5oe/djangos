import random
import string


def create_new_id():
    l = ['4']
    l += random.sample(string.digits, 7)
    l += random.sample(string.digits, 7)
    return ''.join(l)
