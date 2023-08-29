# source: questabox
# related to https://edabit.com/challenge/vFFsWbTX2JuvjKZvf

def print_list(n):
	result = []
	for i in range(n): # alternative: range(1, n+1)
		result.append(i + 1) # alternative: result.append(i)
	return result

print(print_list(1)) # [1]
print(print_list(3)) # [1, 2, 3]
print(print_list(6)) # [1, 2, 3, 4, 5, 6]