# Terminal: 'python3 recover_passwords_117353.py "hashes_len6.txt" 6' (6 is the wordlength)

import hashlib
import sys
from pprint import pprint

def recover(filename, wordlength):
    """zu knackende Hashcodes einlesen"""

    hash_codes = []
    with open(filename, "r") as hashfile:
        for line in hashfile:
            hash_codes.append(line.strip())

    check_hash(hash_codes, wordlength)

def check_hash(hash_codes, wordlength):
    """Wörterbuchangriff"""

    """Vorgehen zum Erstellen des Wörterbuchs: 
    Es gibt 26^Wortlänge mögliche Buchstabenkombinationen der Länge "Wortlänge".
    i wird hochgezählt bis dorthin und alle Zahlen zwischen dort und 0 werden 
    in der 'convert()' Funktion in ein 26-basiertes System umgerechnet.
    Statt Zahlen benutzt man den sich an diesem Index im Alphabet befindlichen 
    Buchstaben. So erstellt man alle möglichen Buchstabenkombinationen der 
    angegebenen Länge."""
    
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z"]
    results = {}

    for i in range(0, (len(alphabet)** wordlength)): #-1? Aber python hört eh immer 1 früher auf!
        word = convert(i, wordlength, alphabet)
        print(i, " = ", word)
        for hash_code in hash_codes:
            if hashlib.sha1(word.encode()).hexdigest() == hash_code:
                results[hash_code] = word
                print("The password from ", hash_code, "is: ", word)
                break

        if len(results) == len(hash_codes):
            print("\nHere are the results as 'hash': 'password'\n")
            pprint(results)
            break

    if results and (len(results) != len(hash_codes)):
        print("\nHere are the results as 'hash': 'password'\n")
        pprint(results)
        for code in hash_codes:
            if code not in results.keys():
                print("But ", code, " could not be resolved.\n")

    elif not results:
        print("Failed completely!")
    

def convert(number, number_digets, alphabet):
    """convert number to a 26-based letter system"""
    """ number = number to convert, number_digets = number of digets"""
    length = len(alphabet)
    word = ""

    while number_digets > 0:
        i = number % length
        word += alphabet[i]
        number //= length
        number_digets -= 1

    return word

def error():
    """Error-Function in case of false userinput"""

    if len(sys.argv) != 3:
        print('ERROR: \n',
              'Please enter a valid path to the hashfile \n',
              'and the expected length of the password (e.g. 6).')
        sys.exit(1)

def main():
    
    error()
    filename = sys.argv[1]
    wordlenghth = int(sys.argv[2])

    recover(filename, wordlenghth)

if __name__ == '__main__':
    main()

