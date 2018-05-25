#!/usr/bin/env python3
'''Need the string statements to explain, leave me alone, pylint -.-'''

''' Terminal: python3 ddt.py "sbox.txt" 
    bzw       python3 ddt.py "sbox4.txt" für Nr. 4 a) '''

import sys
#from pprint import pprint

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

    print("SBOX:")
    print(sbox)
    print("\n")
    create_ddt(sbox)


def create_ddt(sbox):
    '''create ddt by testing all possible inputs'''

    size = len(sbox)
    delta_in = []
    delta_out = []
    x_werte = []


    for y_i in range(0, size):
        delta_in.append(y_i)
        delta_out.append(y_i)
        x_werte.append(y_i)

    ddt_s = [[0 for x in range(size)] for y in range(size)]

    for a_i in delta_in:
        for b_i in delta_out:
            for x_i in x_werte:
                if (sbox[x_i] ^ sbox[x_i ^ a_i]) == b_i:
                    ddt_s[b_i][a_i] += 1

    print_ddt(ddt_s, size)


def print_ddt(ddt, size):
    '''
    print the ddt so it is readable
    '''

    output = [[0 for x in range(size+1)] for y in range(size+1)] # w x h

    '''add delta_in in first row and delta_out in first column'''
    for w_i in range(0, size+1):
        for h_i in range(0, size+1):
            if w_i == 0 and h_i == 0:
                output[w_i][h_i] = 0
            elif w_i == 0 and h_i != 0:
                output[w_i][h_i] = h_i - 1
            elif h_i == 0 and w_i != 0:
                output[w_i][h_i] = w_i - 1
            else:
                output[w_i][h_i] = ddt[w_i - 1][h_i - 1]

    '''fill with 2 digit numbers'''
    for w_i in range(0, size+1):
        for h_i in range(0, size+1):
            output[w_i][h_i] = (str(output[w_i][h_i])).zfill(2)


    print("DDT:")
    for w_i in range(0, size+1):
        for h_i in range(0, size+1):
            print(output[w_i][h_i], end=" ")
            if h_i == size:
                print("\n")


def error():
    """Error-Function in case of false userinput"""

    if len(sys.argv) != 2:
        print('ERROR: \n',
              'Please enter a valid path to the sbox.txt (without -i please)')
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
