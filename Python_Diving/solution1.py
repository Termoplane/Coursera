import sys 
from math import sqrt, pow
a = int(sys.argv[1]) 
b = int(sys.argv[2]) 
c = int(sys.argv[3])

D = pow(b, 2) - 4*a*c

d = sqrt(D)

x1 = (-b + d)/(2*a)
x2 = (-b - d)/(2*a)
print(int(x1), '\n', int(x2), sep='')