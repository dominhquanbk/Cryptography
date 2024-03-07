import math
import re
import time

import matplotlib.pyplot as plt

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

ENGLISH_WORDS = []
start_time = time.time()


# load english words:
def get_data():
    try:
        with open("../words_alpha.txt", 'r') as dictionary:
            for word in dictionary:
                # remove trailing newline characters
                ENGLISH_WORDS.append(word.strip())
            # sorted array for binary search
            ENGLISH_WORDS.sort()
    except IOError:
        print("Error: Unable to read the file.")


def encrypt_rail_fence(text, rails):
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    direction = 1  # Direction of movement: 1 for down, -1 for up
    row, col = 0, 0

    for char in text:
        fence[row][col] = char
        row += direction

        if row == 0 or row == rails - 1:
            direction *= -1  # Change direction when reaching the top or bottom rail

        col += 1

    # Flatten the 2D fence into a 1D list and concatenate all characters
    return ''.join(char for row in fence for char in row)


def decrypt_rail_fence(cipher, key):
    if key <= 1 or key >= len(cipher):
        return cipher

    if key > math.ceil(len(cipher) / 2):
        skip_index = 2 * key - len(cipher) - 1
        return cipher[0: skip_index] + decrypt_rail_fence(cipher[skip_index:], key - skip_index)

    # matrix filled with \n to differentiate space with blank
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]

    # direction of movement
    dir_down = False
    row, col = 0, 0
    index = 0

    # mark the places with '*'
    for i in range(len(cipher)):
        # place the marker
        rail[row][col] = "*"

        # check flow direction
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        # find the next row
        if dir_down:
            row += 1
        else:
            row -= 1

        # next col
        col += 1

    # fill the rail matrix
    for i in range(key):
        for j in range(len(cipher)):
            if (rail[i][j] == '*') and (index < len(cipher)):
                rail[i][j] = cipher[index]
                index += 1

    # read the matrix in zigzag manner then construct the resultant text
    result = []
    dir_down = False
    row, col = 0, 0

    for i in range(len(cipher)):
        # place the marker
        # if rail[row][col] != '*':
        result.append(rail[row][col])

        # check flow direction
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        # find next row
        if dir_down:
            row += 1
        else:
            row -= 1

        # next col
        col += 1

    return "".join(result)


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


def check_english_word(word):
    # regular expression check for uppercase character locations and special character
    if not re.search("^[\"(]?[A-Za-z][a-z]*(-[a-z]+)*(\'([stdm]|ll))?[.,:;\")!?]?$", word):
        return False
    else:
        # lowercase the word
        processed_word = word.lower()
        # remove acronym (n't, 'll, 'd, 's)
        processed_word = re.sub('n\'t', '', processed_word)
        processed_word = re.sub('\'([sdm]|ll)', '', processed_word)
        # remove special character
        processed_word = re.sub('[^A-Za-z0-9]+', '', processed_word)

        if binary_search(ENGLISH_WORDS, 0, len(ENGLISH_WORDS) - 1, processed_word) != -1:
            return True


def prerequisite_check(text):
    # high text length is required for stability(no proof)
    if len(text) < 1000:
        return 0

    text_array = text.split(" ")
    reverse_character_count = 0
    score = 0

    # guarantee last 20 words
    i = 0
    while i < len(text_array) and (score > 0.8 or i < 20):
        word = text_array[i]

        if check_english_word(word):
            score = (score * i + 1) / (i + 1)
        else:
            score = score * i / (i + 1)

        reverse_character_count += len(word)
        i += 1

    return reverse_character_count


def get_english_score(text):
    sample_index = min(len(text), 1000)

    # sorted word array of sampled text
    sample_array = text.split(" ")
    english_count = 0

    for word in sample_array:
        if check_english_word(word):
            english_count += 1

    return english_count / len(sample_array)


def crack(message):
    # store list of all possible value
    score_list = []
    candidate_list = []
    bound_offset = math.ceil(len(message) / 20)
    print("Message length is {}".format(len(message)))

    prerequisite_score = prerequisite_check(message) / len(message)
    print("Prerequisite score is {}".format(prerequisite_score))
    key_left_bound = math.ceil((prerequisite_score + 1) * len(message) / 2) \
        if prerequisite_score > 0.2 else 0
    key_right_bound = len(message) \
        if (len(message) < 1000 or prerequisite_score > 0.2) \
        else min(math.ceil((prerequisite_score + 1) * len(message) / 2) + bound_offset, len(message))

    print("Left bound is {0}, right bound is {1}".format(key_left_bound, key_right_bound))

    key = key_left_bound
    key_nearby = False
    while key < key_right_bound:
        decrypted_text = decrypt_rail_fence(message, key)
        score = get_english_score(decrypted_text)

        # set flag to stop the loop early
        if score > 0.85:
            if not key_nearby:
                key_nearby = True
                key_right_bound = min(key + bound_offset * 2, len(message))
            candidate_list.append((key, score))

        score_list.append((key, score))

        print("Finished key {0}, score: {1}".format(key, score))
        key += 1

    # plot
    plt.plot([pair[0] for pair in score_list], [pair[1] for pair in score_list])
    plt.show()

    # sort to get the key with the highest words count
    candidate_list = sorted(candidate_list, key=lambda x: x[1], reverse=True)
    print(candidate_list)
    if len(candidate_list) > 0:
        print("The key is likely %s" % candidate_list[0][0])
        print(decrypt_rail_fence(message, candidate_list[0][0]))
    else:
        print("No key found!")


# get plaintext
with open('plaintext.txt', 'r') as file:
    # Read the entire content of the file
    plain_text = file.read()

encrypted_text = encrypt_rail_fence(plain_text, 5600)
get_data()
# print(prerequisite_check(encrypted_text))
crack(encrypted_text)
print("--- %s seconds ---" % (time.time() - start_time))
