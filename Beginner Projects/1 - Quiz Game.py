

print("Welcome to my quiz game")

playing = input("Do you want to play? ")

if playing.lower() != "yes":
    quit()

print("Okay! Let's play")

score = 0

answer = input("What does CPU stand for? ")

if answer == "central processing unit":
    score = score + 1
    print('Correct. Your score is ', score)
else:
    print('Incorrect. Your score is', score)

print("You got " + str(score) + " questions correct")

