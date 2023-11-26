# source: https://edabit.com/challenge/vFFsWbTX2JuvjKZvf

def print_list(n):
	result = [] # alternative: result, i = [], 1
	i = 0
	while i < n:
		result.append(i + 1) # alternative: result += [i + 1] 
		i += 1
	return result

print(print_list(1)) # [1]
print(print_list(3)) # [1, 2, 3]
print(print_list(6)) # [1, 2, 3, 4, 5, 6]