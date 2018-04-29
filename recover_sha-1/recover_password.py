# Terminal: python3 recover_password.py "path/to/file.txt" wordlengt (as int)

import hashlib
import sys
from pprint import pprint

def recover(filename, wordlength):
    """zuerst den File mit den Hashwerten öffnen und Zeile für Zeile einlesen
    und daraus eine Liste mit allen zu knackenden Hash-Codes anlegen"""

    hash_codes = []
    with open(filename, "r") as hashfile:
        for line in hashfile:
            hash_codes.append(line.strip())

    """Liste und Wortlänge übergeben"""
    checkHash(hash_codes, wordlength)


def checkHash(hash_codes, wordlength):

    """Alle möglichen Buchstabenkombinationen der erwarteten Wortlänge zusammenbauen,
    die dann mit sha-1 in hashes umrechnen und mit all den zu knackenden aus der
    oben erstellten Liste abgleichen. Bei Treffer in dictionary "result" ablegen"""

    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    results = {}

    for i in range (0, (26** wordlength)-1):
        word = convert(i, wordlength, alphabet)
        print(i, " = ",word)
        for hash in hash_codes:
            if hashlib.sha1(word.encode()).hexdigest() == hash:
                results[hash] = word
                print("The password from ", hash, "is: ", word)
                break
        if len(results) == len(hash_codes):
            print("\nHere are the results as 'hash': 'password'\n")
            pprint(results)
            break

    if (len(results) > 0) and (len(results) != len(hash_codes)):
        print("\nHere are the results as 'hash': 'password'\n")
        pprint(results)
        for code in hash_codes:
            if code not in results.keys():
                print("But ", code, " could not be resolved!\n")

    elif len(results) == 0:
        print("Failed completely!")


def convert(number, n, alphabet):
    # number to convert
    # n = number of digets
    m = len(alphabet)

    word = ""

    while n > 0:
        i = number % m
        word += alphabet[i]
        number //= m
        n -= 1

    return word

def error():
	if len(sys.argv) != 3:
		print('ERROR: Please enter a valid path to the hasfile \n and the expected length of the password.')
		sys.exit(1)

def main():
    args = error()
    f = sys.argv[1]
    w = int(sys.argv[2])

    recover(f, w)

if __name__ == '__main__':
    main()
