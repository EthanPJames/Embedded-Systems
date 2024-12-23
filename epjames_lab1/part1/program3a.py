user_numofterms = int(input("How many Fibonacci numbers would you like to generate? "))

#Get first two fib numbers
fib = []
a = 0
b = 1

#Create Fibonaccui sequence using while loop
index = 0
while index < user_numofterms:
    fib.append(a)
    a, b = b, a + b
    index = index + 1
    
print(fib)