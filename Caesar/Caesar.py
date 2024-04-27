from utility import get_english_score, alphabet


def encrypt_caesar(message, key):
    result = ""
    for x in message:
        if x not in alphabet:
            result += x
        else:
            index = (alphabet.index(x) + key) % 26
            result += alphabet[index]
    return result


def decrypt_caesar(message, key):
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


def crack_caesar(message):
    most_frequent = most_frequent_character(message)
    print('The most frequent letter is {0}'.format(most_frequent))

    for char in frequency_alphabet:
        index = min(1000, len(message))
        key = alphabet.index(most_frequent) - alphabet.index(char)
        result = decrypt_caesar(message[:index], key)
        score = get_english_score(result)

        if score > 0.85:
            print(
                "The correct pair is likely {0} - {1} ({2}), part of the message is:\n{3}".format(most_frequent, char,
                                                                                                  key, result))

        print("Character pair {0} - {1} checked, score: {2}".format(most_frequent, char, score))


def run_caesar(plain_text, key):
    encrypted_message = encrypt_caesar(plain_text, key)
    crack_caesar(encrypted_message)
