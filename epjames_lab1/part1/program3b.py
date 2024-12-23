import random

rand_num = random.randint(0,10) #Get random number
#print (rand_num)

guess_one = int(input("Enter your guess: "))
if guess_one == rand_num:
    print("You win") 
elif guess_one != rand_num:
    guess_two = int(input("Enter your guess: "))
    if guess_two == rand_num:
        print("You win")
    else:
        guess_three = int(input("Enter your guess: "))
        if(guess_three == rand_num):
            print("You win")
        else:
            print("You lose")
else:
    print("You lose")
        
    