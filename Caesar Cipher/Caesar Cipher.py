alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ENGLISH_WORDS=set()
#load english words:
# def get_data():
#     dictionary=open("D:\Code\Cryptography\Caesar Cipher\words_alpha.txt",'r')
#     for word in dictionary.read().split('\n'):
#         ENGLISH_WORDS.append(word)
#     dictionary.close()
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

    if (float(matches)/len(text.split(' ')))*100>=60:
        return True
    return False


def encrypt(message,key):
    message=message.lower()
    result=""
    for x in message:
        if x not in alphabet:
            result+=x
        else:
            index=(alphabet.index(x)+key)%26
            result+=alphabet[index]
    return result

def decrypt(message,key):
    message=message.lower()
    result=""
    for x in message:
        if x not in alphabet:
            result+=x
        else:
            index=(alphabet.index(x)-key)%26
            result+=alphabet[index]
    return result
def crack(message):
    for key in range(len(alphabet)):
        result=decrypt(message,key)    
        if (check_is_english(result)):
            print("the key is likely %s, and the message is %s" %(key,result))
            break
with open('D:\\Code\\Cryptography\\Caesar Cipher\\UTF-8\\example.txt', 'r') as file:
    # Read the entire content of the file
    plain_text = file.read()        
get_data()

encrypted_message=encrypt(plain_text,4)
print(encrypted_message)
crack(encrypted_message)
# print(encrypt("This online utility encodes Unicode data to UTF-8 encoding. Anything that you paste or enter in the input area automatically gets converted to UTF-8 and is printed in the output area. It supports all Unicode symbols and it works with emoji characters. You can choose binary, octal, decimal, or hexadecimal output base for UTF-8 bytes or set an arbitrary base. You can also adjust the delimiter between the bytes and add a byte prefix",5))
#crack("YMNX TSQNSJ ZYNQNYD JSHTIJX ZSNHTIJ IFYF YT ZYK-8 JSHTINSL. FSDYMNSL YMFY DTZ UFXYJ TW JSYJW NS YMJ NSUZY FWJF FZYTRFYNHFQQD LJYX HTSAJWYJI YT ZYK-8 FSI NX UWNSYJI NS YMJ TZYUZY FWJF. NY XZUUTWYX FQQ ZSNHTIJ XDRGTQX FSI NY BTWPX BNYM JRTON HMFWFHYJWX. DTZ HFS HMTTXJ GNSFWD, THYFQ, IJHNRFQ, TW MJCFIJHNRFQ TZYUZY GFXJ KTW ZYK-8 GDYJX TW XJY FS FWGNYWFWD GFXJ. DTZ HFS FQXT FIOZXY YMJ IJQNRNYJW GJYBJJS YMJ GDYJX FSI FII F GDYJ UWJKNC")