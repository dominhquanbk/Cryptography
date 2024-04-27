import os
import sys
import time

from utility import alphabet

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR)
sys.path.append(CURRENT_DIR + '\\RailFence')
sys.path.append(CURRENT_DIR + '\\Caesar')
from Caesar import encrypt_caesar, crack_caesar, run_caesar, most_frequent_character, frequency_alphabet, decrypt_caesar
from RailFence import encrypt_rail_fence, crack_rail_fence, run_rail_fence


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
            print("The correct caesar pair likely is {0} - {1} ({2}), rail fence key is {3}".format(
                most_frequent, char, key, result))
            return


def run_both(plain_text, rail_key, caesar_key):
    encrypted_message = encrypt_both(plain_text, rail_key, caesar_key)
    crack_both(encrypted_message)


def main():
    while True:
        # cipher selection
        print("////////// SELECT CIPHER (text is taken from text.txt ////////////")
        print("1. Caesar")
        print("2. Rail Fence")
        print("3. Both")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1' or choice == '2' or choice == '3':
            # action and action validation
            print("///// Select action: /////")
            print("1. Encrypt text")
            print("2. Crack text")
            print("3. Encrypt and crack text")
            action = input("Enter your choice: ")
            if not (action == "1" or action == "2" or action == "3"):
                print("Invalid action")
                continue

            # key and key validation
            key1 = "0"
            key2 = "0"
            if action != "2":
                if choice == '1' or choice == '3':
                    key1 = input("/// Enter caesar key(number): ")
                if choice == '2' or choice == '3':
                    key2 = input("/// Enter rail fence key(number): ")
                if not key1.isdigit() or not key2.isdigit():
                    print("Invalid key")
                    continue
                key1 = int(key1)
                key2 = int(key2)

            # run
            start_time = time.time()
            with open(CURRENT_DIR + '\\text.txt', 'r') as file:
                # Read the entire content of the file
                text = file.read()

            print("Text length is: {}".format(len(text)))

            encrypt_text = ""
            # encrypt only
            if action == "1":
                if choice == "1":
                    encrypt_text = encrypt_caesar(text, key1)
                elif choice == "2":
                    encrypt_text = encrypt_rail_fence(text, key2)
                else:
                    encrypt_text = encrypt_both(text, key2, key1)
                print("Encrypted text is is:\n{}".format(encrypt_text))
            # crack from input
            if action == "2":
                if choice == "1":
                    crack_caesar(text)
                elif choice == "2":
                    crack_rail_fence(text)
                else:
                    crack_both(text)
            # encrypt and crack
            elif action == "3":
                if choice == "1":
                    run_caesar(text, key1)
                elif choice == "2":
                    run_rail_fence(text, key2)
                else:
                    run_both(text, key2, key1)

            print("--- %s seconds ---" % (time.time() - start_time))

        elif choice == '4':
            break
        else:
            print("Invalid answer")
            continue


main()
