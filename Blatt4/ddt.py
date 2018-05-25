import sys
from pprint import pprint

def read_file(filename):
    '''
    read in the SBOX
    '''

    sbox = []
    with open(filename, "r") as file:
        for line in file:
            box = (line.strip()).split(",")

            for x in box:
                sbox.append(int(x))

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
    

    for y in range(0, size):
        delta_in.append(y)
        delta_out.append(y)
        x_werte.append(y)

    ddt_s = [[0 for x in range (size)] for y in range(size)]

    for a in delta_in:
        for b in delta_out:
            for x in x_werte:
                if ((sbox[x] ^ sbox[x ^ a]) == b):
                    ddt_s[b][a] += 1
    
    #output needs a litte more formating I guess
    print("DDT:")
    pprint(ddt_s)
    print("\n")

def error():
    """Error-Function in case of false userinput"""

    if len(sys.argv) != 2:
        print('ERROR: \n',
              'Please enter a valid path to the sbox.txt (without -i please)')
        sys.exit(1)


def main():
    
    error()
    filename = sys.argv[1]

    read_file(filename)

if __name__ == '__main__':
    main()