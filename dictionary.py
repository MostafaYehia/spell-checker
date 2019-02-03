
from sys import argv
words = set()

def check(word):
    return print(f"{word in words}")

def load(dictionary):
    with open(dictionary, 'r') as file:
        for line in file:
            words.add(line.rstrip("\n"))
            pass
    return True

def size():
    return len(words)

def unload():
    return True


load("dictionary.txt")
check("Zurich")
