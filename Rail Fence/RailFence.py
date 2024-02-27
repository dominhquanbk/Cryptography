alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ENGLISH_WORDS=set()
#load english words:
def get_data():
    try:
        with open(r"D:\Code\Cryptography\Caesar Cipher\words_alpha.txt", 'r') as dictionary:
            for word in dictionary:
                ENGLISH_WORDS.add(word.strip())  # Remove trailing newline characters
    except IOError:
        print("Error: Unable to read the file.")
def count_english_word(text):
    #transform into lower
    text=text.lower()
    #split them into list of word
    words=text.split(" ")
    matches=0
    for word in words:
        if word in ENGLISH_WORDS:
            matches+=1
    return matches
def check_is_english(text):
    matches=count_english_word(text)

    if (float(matches)/len(text.split(' ')))*100>=70:
        return True
    return False


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
    encrypted_text = ''.join(char for row in fence for char in row)
    return encrypted_text

def decrypt_rail_fence(cipher, key):
    cipher=cipher.lower()
    # create the matrix to cipher
    # plain text key = rows ,
    # length(text) = columns
    # filling the rail matrix to
    # distinguish filled spaces
    # from blank ones
    rail = [['\n' for i in range(len(cipher))]
                for j in range(key)]
     
    # to find the direction
    dir_down = None
    row, col = 0, 0
     
    # mark the places with '*'
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
         
        # place the marker
        rail[row][col] = '*'
        col += 1
         
        # find the next row
        # using direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
             
    # now we can construct the
    # fill the rail matrix
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if ((rail[i][j] == '*') and
            (index < len(cipher))):
                rail[i][j] = cipher[index]
                index += 1
         
    # now read the matrix in
    # zig-zag manner to construct
    # the resultant text
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
         
        # check the direction of flow
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
             
        # place the marker
        if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1
             
        # find the next row using
        # direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
    return("".join(result))

def crack(message):
    #store list of all possible value
    list_possible=[]
    for key in range(200):
        try:
            result = decrypt_rail_fence(message, key)
            if check_is_english(result):
                list_possible.append((key, count_english_word(result)))   
        except Exception as e:
           
            continue
    #sort to get the key with highest words count
    list_possible=sorted(list_possible,key=lambda x:x[1],reverse=True)
    print(list_possible)
    print("the key is likely %s"%list_possible[0][0])
    print(decrypt_rail_fence(message,list_possible[0][0]))

# Example usage:
# Specify the file path
# Open the file in read mode ('r')
with open('D:\\Code\\Cryptography\\Caesar Cipher\\UTF-8\\example.txt', 'r') as file:
    # Read the entire content of the file
    plain_text = file.read()



encrypted_text = encrypt_rail_fence(plain_text,167)
get_data()
crack(encrypted_text)

