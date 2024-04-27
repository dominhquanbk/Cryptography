import time
import os
import sys
from utility import get_english_score, check_english_word, alphabet

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR)
sys.path.append(CURRENT_DIR + '\\RailFence')
sys.path.append(CURRENT_DIR + '\\Caesar')
from RailFence import encrypt_rail_fence, run_rail_fence, prerequisite_check, crack_rail_fence
from Caesar import encrypt_caesar, run_caesar, most_frequent_character, frequency_alphabet, decrypt_caesar


def encrypt_both(text, rail_key, caesar_key):
    return encrypt_caesar(encrypt_rail_fence(text, rail_key), caesar_key)


def crack_both(message):
    most_frequent = most_frequent_character(message)
    print('The most frequent letter is {0}'.format(most_frequent))

    for char in frequency_alphabet:
        key = alphabet.index(most_frequent) - alphabet.index(char)
        post_caesar = decrypt_caesar(message, key)
        print("Checking character pair {0} - {1}, initiate rail fence crack".format(most_frequent, char))

        result = crack_rail_fence(post_caesar)
        if result != -1:
            print("The correct caesar pair is {0} - {1} ({2}), rail fence key is {3}".format(
                most_frequent, char, key, result))
            return


def run_both(plain_text, rail_key, caesar_key):
    encrypted_message = encrypt_both(plain_text, rail_key, caesar_key)
    crack_both(encrypted_message)


def main():
    start_time = time.time()
    with open(CURRENT_DIR + '\\plaintext.txt', 'r') as file:
        # Read the entire content of the file
        plain_text = file.read()

    print("Plaintext length is {}".format(len(plain_text)))
    # encrypted_text = encrypt_both(plain_text, 3000, 17)
    # print(encrypted_text)
    run_both(plain_text, 600, 17)

    print("--- %s seconds ---" % (time.time() - start_time))


main()
