# source: https://edabit.com/challenge/pZ3HxBfvejsvkEDo4

def less_than_100(a, b):
    if a + b < 100: # alternative: sum([a, b])
        return True
    else:
        return False

print(less_than_100(22, 15)) # True
print(less_than_100(83, 34)) # False
print(less_than_100(3, 77)) # True