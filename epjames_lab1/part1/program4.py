# Create a dictionary with 5 names and birthdays
birthdays = {
    "Albert Einstein": "03/14/1879",
    "Benjamin Franklin": "01/17/1706",
    "Ada Lovelace": "12/10/1815",
    "Isaac Newton": "01/04/1643",
    "Marie Curie": "11/07/1867"
}

# Welcome message
print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in birthdays.keys():
    print(name)

# Ask the user for the name they want to look up
name = input("Whose birthday do you want to look up?\n")

#Print birthday of person
if name in birthdays:
    print(f"{name}'s birthday is {birthdays[name]}")
else:
    print(f"Sorry, we don't have the birthday information for {name}.")