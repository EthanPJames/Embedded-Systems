import datetime

# Get the current year
current_year = datetime.datetime.now().year
#print(current_year)

# Ask for user's name and age
name = input("What is your name? ")
age = int(input("How old are you? "))

# Calculate the year the user will turn 100
year_turning100 = current_year + (100 - age)

# Print the result
print(f"{name} will be 100 years old in the year {year_turning100}")
