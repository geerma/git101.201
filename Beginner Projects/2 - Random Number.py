import random

random_number = random.randrange(-1,10)

guess = input("Guess the number: ")
guesses = 0

if guess.isdigit():
    guess = int(guess)

else:
    print("Input a number")
    quit()

while guess != random_number:
    ##if guess == random_number:
    ##    print ("Correct")
        
    
    if guess > random_number:
        print ("Your guess is higher than the number. Guesses:", guesses)
        guess = input("Guess another number: ")
        if guess.isdigit():
            guess = int(guess)
        guesses = guesses + 1

    else:
        print ("Your guess is lower than the number", guesses)
        guess = input("Guess another number: ")
        if guess.isdigit():
            guess = int(guess)
        guesses = guesses + 1
        
        
if guess == random_number: 
    print ("Correct")
    


