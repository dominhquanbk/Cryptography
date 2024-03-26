import re

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

ENGLISH_WORDS = []


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


def get_english_score(text):
    # sorted word array of sampled text
    sample_array = text.split(" ")
    english_count = 0

    for word in sample_array:
        if check_english_word(word):
            english_count += 1

    return english_count / len(sample_array)


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
