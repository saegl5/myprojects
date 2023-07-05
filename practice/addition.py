# source: https://edabit.com/challenge/rZToTkR5eB9Zn4zLh

def addition(a, b):
    return a + b

print(addition(3, 2)) # 5
print(addition(-3, -6)) # -9
print(addition(7, 3)) # 10

# alternative

a = 3
b = 2

def addition(a, b): # could also use different variables
    return a + b

print(addition(a, b)) # 5
# repeat for a = -3 and b = -6 # -9
# repeat for a = 7 and b = 3 # 10