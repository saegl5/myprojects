# source: https://edabit.com/challenge/rZToTkR5eB9Zn4zLh

# simplest

def addition(a, b):
    print(a + b)

addition(3, 2) # 5
addition(-3, -6) # -9
addition(7, 3) # 10

# alternative using `return`

def addition(a, b):
    return a + b

print(addition(3, 2)) # 5
print(addition(-3, -6)) # -9
print(addition(7, 3)) # 10

# alternative using `global`

s = int()

def addition(a, b):
    global s
    s = a + b

addition(3, 2); print(s) # 5
addition(-3, -6); print(s) # -9
addition(7, 3); print(s) # 10