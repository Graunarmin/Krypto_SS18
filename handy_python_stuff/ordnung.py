'''
findet die Ordnung des Elements a in Z_p mit neutralem Element e

ord(a) = {min(n € N | a**n = e), falls existent, sonst unendlich}
'''

def ordnung(a, p, e):
    found = False
    for n in range(1, p):
        if ((a ** n) % p) == e :
            #print(n)
            found = True
            return n
    
    if not found:
        print("infinitive")
        return(-1)


def main ():
    
	a = int(sys.argv[1])
	p = int(sys.argv[2])
	e = int(sys.argv[3])
	
	
	Ordnung(a, p, e) 
	
if __name__ == '__main__':
    main()