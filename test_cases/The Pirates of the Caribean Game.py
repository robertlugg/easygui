"""
from:
https://code.google.com/p/piratesofthecaribbeangame/
"""
import sys

sys.path.append('..')
import easygui

import random

secret = random.randint(1,99)
guess = 0
tries = 0

name = easygui.enterbox("Arrg its me Davy Jones whats your name ye scallywab")
txt = "Do you fear DEATH {}? Lets play a game if ye win ye can go if ye lose"
txt += " then you are my a sailer on my ship the flying dutchman forever AHAAAA!"
easygui.msgbox(txt.format(name))
easygui.msgbox("The game be simple ye get 15 chances to guess a number between 1 and 100. Ye be ready?")

while guess != secret and tries < 15:
    guess = easygui.integerbox("What's your guess "+name)
    if not guess: break
    if guess < secret:
        easygui.msgbox(str(guess) + " is too low "+name)
    elif guess > secret:
        easygui.msgbox(str(guess) + " is too high "+name)

    tries += 1
    
    if guess == secret:
        easygui.msgbox("Arrg ye got it in {}.  You can go.".format(tries))
    if tries == 15:
        easygui.msgbox("NO more guesses for ye.  You're mine forever now {} !! AHAAHAA!!!".format(name))
        
