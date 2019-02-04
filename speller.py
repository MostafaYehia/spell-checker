import re
import time
from sys import argv, exit
from dictionary import load, unload, check, size

DICTIONARY = "dictionary.txt"

argc = len(argv)
LENGTH = 45

if argc != 2 and argc != 3:
    exit("You should includ file at least")

time_load, time_check, time_size, time_unload = 0.0, 0.0, 0.0, 0.0
dictionary = argv[1] if argc == 3 else DICTIONARY


#################
# Load dictionary
#################

before = time.process_time()
loaded = load(dictionary)
after = time.process_time()
if not load:
    exit("Could not load {dictionary}")
time_load = after - before

#######################################
# Load text file to check its spellings
#######################################
text = argv[-1]

print(f"File to check {text}")

# Open text file
with open(text, 'r', encoding='latin-1') as file:
    if not file:
        # print(f"Could not load {text}")
        # Unload load dictionary from MEMORY ( Free Memory )
        unload()
        exit(1)

    index, start, misspellings, words = 0, 0, 0, 0

    word = ""
    # assemples words from the file
    while True:
        c = file.read(1)
        if not c:
            break

        if re.match(r"[A-Za-z]", c) or (c == "'" and index > 0):
            word += c
            # print("Word now: ", word)
            index += 1


            if index > LENGTH:

                while True:
                    c = file.read(1)
                    if not c or not re.match(r"[A-Za-z]", c):
                        # print("This is not character: ",  c)
                        break

                index, word = 0, ""

        elif c.isdigit():
            while True:
                c = file.read(1)
                if not c or (not c.isalpha() and not c.isdigit()):
                    break

                index, word = 0, ""

        elif index > 0:

            words += 1

            before = time.process_time()
            misspelled = not check(word)
            after = time.process_time()

            time_check = after - before

            if misspelled:
                end = start + len(word)
                print(f"Misspelled word {word} at {start}:{end}")
                misspellings += 1

            index, word = 0, ""

        start += 1

##########################################
# Count the words in the loaded dictionary
##########################################
before = time.process_time()
n = size()
after = time.process_time()
time_size = after - before


####################################################
# Finaly Unload dictionary from MEMORY (Free Memory)
####################################################

before = time.process_time()
unloaded = unload()
after = time.process_time()
if not unloaded:
    exit(f"Could not unload {dictionary}")
time_unload = after - before


# Print results
print(f"\nWORDS MISSPELLED:   {misspellings}")
print(f"WORDS IN DICTIONARY:   {n}")
print(f"WORDS IN TEXT:   {words}")
print(f"TIME IN load:   {time_load:.2f}")
print(f"TIME IN check:   {time_check:.2f}")
print(f"nTIME IN size:   {time_size:.2f}")
print(f"TIME IN unload:   {time_unload:.2f}")
print(
    f"TOTAL TIME:   {(time_load + time_check + time_size + time_unload):.2f}")


# End the program with success flag
exit(0)
