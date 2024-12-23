import random

# Initialize the list with 10 random numbers between 1 and 100
a = [random.randint(1, 100) for _ in range(10)]
print(a)

# Ask the user for a number and convert it to an integer
user_number = int(input("Enter number: "))

b = []
for num in a:
    # If the number in `a` is smaller than the user's number, add it to the list `b`
    if num < user_number:
        b.append(num)

# Print the new list
print(f"The new list is {b}")

    
    
