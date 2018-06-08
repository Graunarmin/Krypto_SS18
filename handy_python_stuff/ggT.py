'''
ggT von s und e auf verschiedene Weisen bestimmen, bevorzugt euk_it oder euk
'''

import time
import sys


def brut(s,e):
	if s > e:
		min = e
	else:
		min = s
	for i in range (min, 0, -1):
		if s % i == 0 and e % i == 0:
			#print (i)
			return i

def euk(s,e):
	r = s % e
	if r == 0:
		#print(e)
		return e
	else:
		s = e
		e = r
		#print(e)
		return e

def euk_it(s,e):
	tmp = 0

	if s < e:
		tmp = e
		e = s
		s = tmp

	while True:
		r = s % e
		if r == 0:
			break
		s = e
		e = r
	#print (e)
	return e


#Versionen zur Eingabe von Start und Ende, ggT von 2^k, (2^k)-1

def brutal(s,e):
	for k in range (s, e + 1):
		t1 = time.time()
		for i in range (e, s -1, -1):
			if (2**k)% i == 0 and ((2**k)-1) % i == 0:
				t2 = time.time()
				t = t2 - t1ew
				print ("ggT((2^",k,"),((2",k,")-1)) = ",i)
				print ("Rechenzeit =",t)



def euklid(s,e):
	for k in range (s, e + 1):
		t1 = time.time()
		a = 2**k
		b = (2**k) - 1
		r = a % b
		if r == 0:
			t2 = time.time()
			t = t2 - t1
			print("ggT(2 ^",k,", (2 ^",k,")-1) =",b)
			print("Rechenzeit =",t)
		else:
			a = b
			b = r
			t2 = time.time()
			t = t2 - t1
			print("ggT(2 ^",k,", (2 ^",k,")-1) =",b)
			print("Rechenzeit =",t)

def error():
	if len(sys.argv) != 3:
		print('Please enter two numbers.')
		sys.exit(1)
	
	try: 
		s = int(sys.argv[1])
		e = int(sys.argv[2])
	except ValueError:
		print('Please enter two integers')
		sys.exit(1)


def main():

	args = error()
	s = int(sys.argv [1])
	e = int(sys.argv[2])

	# brut(s,e)
	# euk(s,e)
	# euk_it(s,e)

	#brutal(s,e)
	#euklid(s,e)
	
	
if __name__ == '__main__':
    main()



