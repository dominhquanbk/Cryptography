import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)
from utility import get_english_score, get_data, alphabet

start_time = time.time()


def encrypt(message, key):
    result = ""
    for x in message:
        if x not in alphabet:
            result += x
        else:
            index = (alphabet.index(x) + key) % 26
            result += alphabet[index]
    return result


def decrypt(message, key):
    result = ""
    for x in message:
        if x not in alphabet:
            result += x
        else:
            index = (alphabet.index(x) - key) % 26
            result += alphabet[index]
    return result


def most_frequent_character(text):
    return sorted([(a.lower(), text.count(a) if a.lower() in alphabet else 0) for a in text],
                  key=lambda x: x[-1])[-1][0]


frequency_alphabet = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'y', 'w', 'g', 'p', 'b',
                      'v', 'k', 'x', 'q', 'j', 'z']


def crack(message):
    most_frequent = most_frequent_character(message)
    print('The most frequent letter is {0}'.format(most_frequent))

    for char in frequency_alphabet:
        index = min(1000, len(message))
        key = alphabet.index(most_frequent) - alphabet.index(char)
        result = decrypt(message[:index], key)
        score = get_english_score(result)

        if score > 0.85:
            print("The key is likely %s, part of the message is %s" % (key, result))

        print("Key {0} passed, score: {1}".format(key, score))


# get plaintext
with open(CURRENT_DIR + '\\plaintext.txt', 'r') as file:
    # Read the entire content of the file
    plain_text = file.read()
encrypted_message = encrypt(plain_text, 17)
get_data()

crack(encrypted_message)
print("--- %s seconds ---" % (time.time() - start_time))
