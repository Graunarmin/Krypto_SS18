import sys

def to_hex(number):
        
    key = ""
    length = 4

    base = ['0', '1', '2', '3', '4', '5', '6', '7', 
            '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    
    while length > 0:
        i = number % 16
        key += base[i]
        number //= 16
        length -= 1
    
    return key[::-1]

def main():
    
    n = int(sys.argv[1])

    print(to_hex(n))

if __name__ == '__main__':
    main()

    
    

            
            
        


