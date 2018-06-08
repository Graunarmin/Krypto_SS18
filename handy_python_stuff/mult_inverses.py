'''
Multiplikatives Inverses von x in Zn bestimmen
'''

import sys
import ggT

def mult_inv(x, Z_n):
    if ggT.euk_it(x, Z_n) == 1:
        for i in range (0, Z_n +1):
            if ((i * x) % Z_n) == 1:
                print(i)
                return i

def main():
    
	x = int(sys.argv [1])
	Z_n = int(sys.argv[2])

	#mult_inv(x, Z_n)
	
if __name__ == '__main__':
    main()


