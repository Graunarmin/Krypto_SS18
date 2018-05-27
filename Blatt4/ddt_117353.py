#!/usr/bin/env python3
# Valerie Lemuth (117017) & Johanna Sacher (117353)

''' Terminal: python3 ddt_117353.py sbox.txt
    bzw für 4a): python3 ddt_117353.py sbox4.txt '''

import sys

def read_file(filename):
    '''
    read in the SBOX
    '''

    sbox = []
    with open(filename, "r") as file:
        for line in file:
            box = (line.strip()).split(",")
            for x_i in box:
                sbox.append(int(x_i))

    print("SBOX:", sbox, "\n")
    create_ddt(sbox)


def create_ddt(sbox):
    '''
    create ddt by testing all possible inputs
    '''

    size = len(sbox)
    values = [y for y in range(size)]
    ddt_s = [[0 for x in range(size)] for y in range(size)]

    for d_in in values:
        for d_out in values:
            for x_i in values:
                if (sbox[x_i] ^ sbox[x_i ^ d_in]) == d_out:
                    ddt_s[d_out][d_in] += 1

    print_ddt(ddt_s, size)


def print_ddt(ddt, size):
    '''
    print the ddt so it is readable
    add delta_in in first row and delta_out in first column and fill with leading zeros
    '''

    output = [[0 for x in range(size+1)] for y in range(size+1)] # w x h

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

    print("DDT:")
    for w_i in range(0, size+1):
        for h_i in range(0, size+1):
            print(output[w_i][h_i], end=" ")
            if h_i == size:
                print("\n")

def error():
    '''
    Error-Function in case of false userinput
    '''

    if len(sys.argv) != 2:
        print('ERROR: \n',
              'Please enter a valid path to the "sbox.txt" (without -i please)')
        sys.exit(1)


def main():
    '''
    generate DDT for given sbox of variable length
    '''

    error()
    filename = sys.argv[1]

    read_file(filename)

if __name__ == '__main__':
    main()
