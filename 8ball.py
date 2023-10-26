import math
import random
import time


eightball = ''' .-"""-.
/   _   \\
|  (8)  |
\   ^   /
 '-...-\''''


spacer = '''





'''


answers = ["idk man gl", "I'm not answering that's too political", "nah u good", "you don't need to know dawg", "quit asking stupid questions", "yeah for sure", "girllllll, wtf", "dawg what", "fo sho fo sho", "whateva whateva, I don't wanna answer", "probably, but I didn't check", "just google it", "uhm. No. obviously.", "imagine I wrote the right answer here", "yeah man"]

while True:
    print(eightball)
    print("What would you like to ask the magic 8-Ball?")
    question = input()
    print("h" + "m" * random.randrange(1,50))
    time.sleep(3)
    answerkey = random.randrange(1,len(answers))
    chexquest = random.randrange(1,7)
    if chexquest == 3:
        print("Oh this one is easy")
    else:
        print("That's a tough one....")
    time.sleep(4)
    print(answers[answerkey])
    time.sleep(4)
    print(spacer)
    # print(chr(27) + "[2J")