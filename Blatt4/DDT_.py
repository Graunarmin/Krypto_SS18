import numpy
from pprint import pprint
import sys

def readTxt(path):
    
    with open(path, "r") as file:

        words = []

        for line in file:
            for char in line:
                if char != ",":
                    words.append(int(char))

        return words

def printDdt(ddt, size):
    
    output = numpy.zeros(shape=[size+1, size+1])

    for w_i in range(0, size + 1):
        for h_i in range(0, size + 1):
            if w_i == 0 and h_i == 0:
                output[w_i][h_i] = (str(0)).zfill(2)
            elif w_i == 0 and h_i != 0:
                output[w_i][h_i] = (str(h_i - 1)).zfill(2)
            elif h_i == 0 and w_i != 0:
                output[w_i][h_i] = (str(w_i - 1)).zfill(2)
            else:
                output[w_i][h_i] = (str(ddt[w_i - 1][h_i - 1])).zfill(2)

    print(str(output).replace("[", " ").replace("]", "").replace("."," "))

def DDT(path):
    
    s = readTxt(path)

    ddt = numpy.zeros(shape=[len(s), len(s)])

    for i in range(0, len(s)):
        for j in range(0, len(s)):

            deltaIn = i ^ j

            deltaOut = s[i] ^ s[j]

            ddt[deltaOut][deltaIn] += 1

    printDdt(ddt, len(s))


def main():

    if len(sys.argv) != 2:
        print("Please enter the path to your sbox.txt!")
        sys.exit(1) 

    path = sys.argv[1]          

    DDT(path)

if __name__ == '__main__':
    main()
