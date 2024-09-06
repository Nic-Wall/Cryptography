#https://www.quora.com/What-are-some-ideas-for-simple-cryptography-cryptanalysis-projects
import re
import string
import random
import math
import numpy as np

#Formatting keys and phrases with as lower with no spaces or special characters
def low_no_spec_char(entry):
    entry = entry.lower()
    entry = re.sub(r"([^A-z])", "", entry)
    return entry

#Caesar
def caesar_cipher(phrase = "", fixed_shift= 0, encode= 1):
    """
        The caesar cipher is simply shifting letters a fixed number of positions in a determined direction through the alpahbet. For instance...
        A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
        X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
    """
    phrase = low_no_spec_char(phrase)
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]   #Created before I learned of string.ascii_lowercase
    new_phrase = ""
    if(not encode): #encode
        encode = -1 #decode
    for letter in phrase:
        try:
            new_phrase += str(alphabet[alphabet.index(letter) + (fixed_shift * encode)])
        except:
            new_phrase += str(letter)
    return(new_phrase)

#Rail Fence Cipher
def railFence_cipher(phrase= "", rails= 3, encode= 1):
    """
    
    """
    phrase = low_no_spec_char(phrase)
    if(encode):
        new_phrase_list = ["" for rail in range(0,rails)]
        rail_num = 0
        rail_dir = 0
        for letter in range(0, len(phrase)):    #There is a more effecient way to do this, there must be
            new_phrase_list[rail_num] += str(phrase[letter])
            if(rail_num == 0):
                rail_dir = 1
            if(rail_num == rails-1):
                rail_dir = -1
            rail_num += rail_dir
        new_phrase = ""
        for rail in new_phrase_list:
            new_phrase += rail
        
    elif(not encode):
        new_phrase_list = ["" for letter in range(0, len(phrase))]
        iterator = 0
        gap = rails+(rails%3)+1
        for rail in range(0, rails):
            next_step = gap - (rail * 2)
            for letter in range(rail, len(phrase), gap):
                new_phrase_list[letter] = phrase[iterator]
                iterator += 1
                if((rail != 0) and (rail != rails-1) and ((next_step + letter) <= len(phrase))):
                    new_phrase_list[next_step + letter] = phrase[iterator]
                    iterator += 1
        
        new_phrase = ""
        for letter in new_phrase_list:
            new_phrase += letter
    
    return new_phrase

#Vigenere
def vigenere_cipher(phrase="", key= "", encode= 1):
    """
        The letters of the encoded message are shifted based on the position of the letters from the key phrase in the alphabet. For instance...
        To Encode: attacking tonight
        Key Phrase: oculorhinolaringology
        A > O | 0 + 14 = 14
        T > V | 19 + 2 = 21
        T > N | 19 + 20 = 14 (... w, x, y, z, a, b, c, d...)
        so "attacking tonight" becomes "ovnlqbpvt hznzouz"
    """
    phrase = low_no_spec_char(phrase)
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    new_phrase = ""
    error_correction = 0
    if(not encode):
        encode = -1
    for letter in range(0, len(phrase)):
        try:
            new_phrase += str(alphabet[(alphabet.index(phrase[letter]) + (encode * alphabet.index(key[(letter % len(key)) + error_correction]))) % len(alphabet)])
        except:
            new_phrase += str(phrase[letter])
            error_correction -= 1
    return(new_phrase)

#Playfair
def playfair_cipher(phrase= "", table= [["a", "b", "c", "d", "e"], ["f", "g", "h", "i", "k"], ["l", "m", "n", "o", "p"], ["q", "r", "s", "t", "u"], ["v", "w", "x", "y", "z"]], encode= 1):
    """
        Playfair uses a table to transpose letters based on the position of their pairs.
        Steps:
            - Create a 5x5 table excluding a rarely used letter (such as j)
            - Remove every character that isn't in the table
            - Seperate repeating characters with a null letter (such as x or q)
            - Remove instances of double null variables
            - Split the string into pairs of letters "01", "23", "45", etc.
                - In the event there are an odd number of letters append a null letter "67", "8X"
            - If the final pair is a pair of null letters remove the pair
            - Change the pair of letters based on the following rules...
                - If the pair is on the same row shift each letter over one
                - If the pair is in the same column shift each letter down one
                - If the pair is not in the same column or same row, create a rectangle and assign each letter the value on the same row as itself and the same column as it's partner
        Decoding is the same as encoding EXCEPT
            - Every character that isn't in the table should already be removed
            - Seperate repeating characters shouldn't exist in the phrase (because of the way it's encoded)
            - There should be no instance of double null variables (as they're removed during encryption)
            - Instead of moving values one to the right or down they're moved to the left or right
        For readability the phrase is split into groups of five at the end (which doesn't matter when encoding/ decoding because they're split into pairs before being transformed)
    """
    phrase = low_no_spec_char(phrase)
    if(encode): #Will adjust the size of rectangles if applied to messages requiring decoding. After adjustments made to encode there should be no instance where the below occurs
        phrase = re.sub(r"([A-z])\1", r"\g<1>x\g<1>", phrase)   #Fills in repeating letters with a null value
        phrase = re.sub(r"j", "x", phrase)  #Replaces the one missing letter from the table (j) with a null value (x)
    phrase = re.sub(r"(x)\1", "", phrase)   #In an instance were double x's may occur after filling in nulls, remove them
    phrase_splits = re.findall("([A-z]{1,2})", phrase)  #Creates a list of the pairs
    if(len(phrase_splits[len(phrase_splits)-1]) == 1):  #If the final index of the list is not a pair, make it one with a null variable
        phrase_splits[len(phrase_splits)-1] += "x"
        if(phrase_splits[len(phrase_splits)-1] == "xx"):    #If the final index of the list is a pair of null variables, remove it
            phrase_splits.remove(-1)
    
    #Creates a dictionary of every letter in the table for quick reference
    table_dict = {}
    for line in range(0, 5):    #Returns error if the table size input by the user is out of range
        for letter in range(0, 5):
            if(table[line][letter] in table_dict):
                return "NO REPEAT LETTERS IN THE TABLE ALLOWED"
            table_dict[table[line][letter]] = (line, letter)

    if(not encode):
        encode = -1

    new_phrase = ""
    for duo in phrase_splits:   #Itterating through every pair in phrase_splits created above
        first_locale = table_dict[duo[0]]   #Tuple(line_in, letter_in)
        second_locale = table_dict[duo[1]]
        if(first_locale[0] == second_locale[0]):    #They both exist on the same row, take from their right (encoding) or left (decoding)
            new_phrase += (str(table[first_locale[0]][(first_locale[1]+encode) % 5]) + str(table[second_locale[0]][(second_locale[1]+encode) % 5]))
        elif(first_locale[1] == second_locale[1]):  #They both exist on the same column, take from one directly below (encoding) or above (decoding) each
            new_phrase += (str(table[(first_locale[0]+encode) % 5][first_locale[1]]) + str(table[(second_locale[0]+encode) % 5][second_locale[1]]))
        else:   #They don't exist on the same row OR column, make a rectangle and select from the other pair of corners (vertical or horizontal) depending on the corners made by the original pair
            new_phrase += (str(table[first_locale[0]][second_locale[1]]) + str(table[second_locale[0]][first_locale[1]]))

    new_phrase = re.sub(r"([A-z]{1,5})", r"\g<0> ", new_phrase) #Seperates the phrases with a space between every five characters for readability
    return new_phrase

#Columnar Tranposition
def columnar_transposition(phrase= "", key= "", encode= 1, second_key= ""):
    phrase = low_no_spec_char(phrase)
    key = low_no_spec_char(key)
    key = "".join(set(key))
    while(len(phrase) % len(key) != 0): #Filling in the phrase with random letters to make even sized columns
        phrase += "x" #random.choice(string.ascii_lowercase)
    
    if(encode == 1):
        table = [[] for letter in key]
        for letter in range(0, len(phrase)):    #Filling in the table (columns)
            table[letter%len(key)].append(phrase[letter])
        new_phrase = ""
        for itterator in sorted(key):   #Itterates through each letter in the sorted key
            for letter in table[key.index(itterator)]:  #Itterates through each column (identified by the index of each letter in the origianl key (but in the order of the sorted key))
                new_phrase += letter
        if(second_key != ""):
            new_phrase = columnar_transposition(phrase= new_phrase, key= second_key, encode= 1)
    
    else:
        if(second_key != ""):
            new_phrase = columnar_transposition(phrase= phrase, key= second_key, encode= 0)
        else:
            table = ["" for letter in range(0, len(key))]   #Creating the table to store the ordered columns
            sorted_key = sorted(key)
            for letter_group in range(0, len(phrase), int(len(phrase)/len(key))):
                itterator = key.index(sorted_key[-((letter_group)%len(key))])
                table[itterator] = phrase[letter_group : letter_group + int(len(phrase)/len(key))]
            new_phrase = ""
            for letter in range(0, len(table[0])):
                for column in table:
                    new_phrase += column[letter]

    return new_phrase

#Affine Cipher
def affine(phrase= "", key_a= 0, key_b= 0, encode= 1):
    alphabet = string.ascii_lowercase  #Creating the alphabet to map to
    """
    Encoding is simply (ax + b) % len(alphabet)
    where x is the index of the letter in the alphabet (i.e. A= 0, B= 1, C= 2, etc)
    a MUST BE a coprime of 26 (len(alphabet)) meaning a must be a prime number between 0 and 26 that does not share any common factor except 1 (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, and 25)
    """
    valid_coprimes = [1,3,5,7,9,11,15,17,19,21,23,25]
    if(key_a not in valid_coprimes):    #Raising an error if the provided a_key is not a coprime of 26
        raise Exception("The provided key_a is not a coprime of the alphabet's length (26).")    
    alphabet = string.ascii_lowercase
    phrase = low_no_spec_char(phrase)
    m = len(alphabet)
    #Unlike the caeser cipher I opted for a dictionary to encode each letter making calculations once increases speed the longer the message
    dict_trans = {}
    if(encode):
        for letter in range(0, m):
            dict_trans[alphabet[letter]] = alphabet[((key_a * letter) + key_b) % m]
    else:
        inv_mod = inverse_modulo(m= m, key= key_a)
        for letter in range(0,m):
            dict_trans[alphabet[letter]] = alphabet[((inv_mod) * (letter - key_b)) % m]
    
    new_phrase = ""
    for letter in range(0, len(phrase)):
        new_phrase += dict_trans[phrase[letter]]
    return new_phrase

def inverse_modulo(m= 26, key= 0):
    #Uses the extended euclidean algorithm to find the modular multiplicative inverse of key_a % m
    eq = [m, key] #Starts as m = key_a * x + y
    quo = [None]    #quotient (x)
    rem = [None]    #remainder (y)
    t1 = 0  #Always starts with 0
    t2 = 1  #Always starts with 1
    #GCD (Greatest Common Denominator) and Extended Euclidean Algorithm
    while(rem[-1] != 1):  #Because we're using coprimes of 26, the last position of y[-1] will ALWAYS be 1
        #Calculates the greatest common denominator
        quo.append(math.floor(eq[-2]/eq[-1]))   #Quotient is largest factor of eq[-1] that is less than or equal to eq[-2]
        rem.append(eq[-2] - (quo[-1] * eq[-1])) #Remainder is calculated as eq[-2] - (largest factor of eq[-1] <= eq[-2])
        eq.append(rem[-1])  #The old remainder becomes the new eq
        #Calculates the eventual inverse modulo - m
        #Using this page I learned of t1, t2, and t3: https://stackoverflow.com/questions/10133194/reverse-modulus-operator and https://www.extendedeuclideanalgorithm.com/xea.php
        t3 = t1 - (quo[-1] * t2)    #t3 is calculated with the current quotient t1 and t2
        t1 = t2 #t1 becomes the old t2
        t2 = t3 #t2 becomes the old t3
    inverse_modulo = m + t2
    return inverse_modulo

#Hill Cipher
#I already made a basic linear algebra module in C++ so I opted for the use of numpy for this cipher
def hill(phrase= "", key= np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), encode= 1):
    #Check to make sure the matrix is of an nxn shape
    if(len(key) != len(key[-1])):   #NEED TO COMPARE TO ALL ROWS
        raise Exception("The provided key is not of a nxn shape.")
    key_det = np.linalg.det(key) % 26
    if(key_det == 0 or key_det == 2 or key_det == 13):
        raise Exception("The key's determinent (mod alphabet_length(or 26)) must NOT be equal to 0, 2, or 13 for this cipher, or else decryption is NOT possible.")
    alphabet = string.ascii_lowercase
    key = key % len(alphabet)   #Ensuring the key is of modulus len(alphabet) (26)
    if(encode != 1):    #Decrypt
        #https://www.dcode.fr/matrix-inverse
        det = int(np.linalg.det(key)) % len(alphabet)
        det_inv = pow(det, -1, len(alphabet))
        minors = np.zeros_like(key)
        for i in range(0,3):
            for j in range(0,3):
                minors[i,j] = minors(key, i, j)
        cofactor = minors * np.array([[1,-1,1],[-1,1,-1],[1,-1,1]])
        adjugate = cofactor.T
        key = (det_inv * adjugate) % len(alphabet)
        #Else, the key stays as submitted
    phrase = low_no_spec_char(phrase)
    appended_bs = 0 #Count of b's to append, keeping the phrase sub_vectors an equal length to the key's nxn size
    while (len(phrase) % len(key[0]) != 0):    #Appending b's to the phrase so the vector's length is equal to the key's shape every time (the b's will be added before decryption or removed after encryption)
        phrase += "b"   #Choosing b because it's equal to 1
        appended_bs += 1    #Keeping track so they can be popped at the end of the encryption
    vector_size = int(len(key[-1]))
    new_phrase = ""
    for vector in range(0, len(phrase), vector_size):
        sub_vector = phrase[vector:vector+vector_size]
        num_vector = []
        for letter in sub_vector:
            num_vector.append(alphabet.index(letter))
        num_vector = (key.dot(np.asarray(num_vector))) % len(alphabet)
        for index in num_vector:
            new_phrase += alphabet[index]
    new_phrase = new_phrase[0:len(new_phrase)-appended_bs]  #Removing appended b's
    return new_phrase
def mat_minors(mtrx, i, j):
    minor_matrix = np.delete(np.delete(mtrx, i, axis= 0), j, axis= 1)
    return int(np.round(np.linalg.det(minor_matrix)))

#Enigma Machine Simulator

#One-Time Pad

#AES

#RSA

#Hash Function (SHA-256)

#Transposition


to_encode = "time to study"
encoding_method = 6

if(encoding_method == 0):   #Caesar
    pass_along = caesar_cipher(to_encode, 3, 1)
    print(pass_along)
    pass_along = caesar_cipher(pass_along, 3, 0)
    print(pass_along)

elif(encoding_method == 1): #Rail Fence
    pass_along = railFence_cipher(to_encode, 3, 1)
    print(pass_along)
    pass_along = railFence_cipher(pass_along, 3, 0)
    print(pass_along)

elif(encoding_method == 2): #Vigenere
    key = "oculorhinolaringology"
    pass_along = vigenere_cipher(to_encode, key, 1)
    print(pass_along)
    pass_along = vigenere_cipher(pass_along, key, 0)
    print(pass_along)

elif(encoding_method == 3): #Playfair
    table = [["p", "l", "a", "y", "f"],
             ["i", "r" , "e", "x", "m"],
             ["b", "c", "d", "g", "h"],
             ["k", "n", "o", "q", "s"],
             ["t", "u", "v", "w", "z"]]
    pass_along = playfair_cipher(to_encode, table= table, encode= 1)
    print(pass_along)
    pass_along = playfair_cipher(pass_along, table= table, encode= 0)
    print(pass_along)

elif(encoding_method == 4): #Columnar Transposition
    key= "janeausten"
    second_key = "aeroplanes"
    pass_along = columnar_transposition(phrase= to_encode, key= key, encode= 1)
    print(pass_along)
    pass_along = columnar_transposition(phrase= pass_along, key= key, encode= 0)
    print(pass_along)

elif(encoding_method == 5): #Affine
    key_a = 11
    key_b = 26
    pass_along = affine(phrase= to_encode, key_a= key_a, key_b= key_b, encode= 1)
    print(pass_along)
    pass_along = affine(phrase= pass_along, key_a= key_a, key_b= key_b, encode= 0)
    print(pass_along)

elif(encoding_method == 6): #Hill
    key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    pass_along = hill(phrase= to_encode, key= key, encode= 1)
    print(pass_along)
    pass_along = hill(phrase= pass_along, key= key, encode= 0)
    print(pass_along)

"""
To add:
    - Option for left or right encoding with the Caeser cipher
    - Enigma machine
    - Vigenere cipher working using a key with spaces (just drop the spaces, do they count as 0's, etc?)
        + Based on the tabula recta spaces should be dropped
    - Return an error if the number of rails requested is greater than the number of characters in the phrase
    - Add another option to decrypt without the key (or maybe just another function)
    - In columnar and playfair, need to adjust repeat letter adjustments to account for groups of three rather than just two
"""