def factors(x):
  for i in range(1, x+1):
    if x%i == 0:
      print(i)

# "%" is modulo (i.e., remainder of x divided by i)

def multiples(x, y): # limited
  i = 0
  while i*x <= y:
    print(i*x)
    i += 1
