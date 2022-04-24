__author__ = 'Mays D'

# Ref:
# http://stackoverflow.com/questions/29767777/gui-quiz-using-easygui-and-pygame-issue-with-quieting-the-game-and-playing-sound

#We start by importing a few libraries.
#Easygui provides our GUI for the game.
import sys
sys.path.append('..')   ;# This is only needed in Robert Lugg's development environment

from easygui import *
#Time is a library that introduces the concept of time to the game.
import time
#Pygame is a series of multimedia tools that can create games using Python.
import pygame

#To start pygame we need to initialise it.
pygame.init()
#To use the audio facilities of Pygame we need to tell Pygame that we wish to use them.
pygame.mixer.init()

#Now we create three functions, these functions contain the code to play each audio track.
#The audio for each of these functions should be in the same folder as this code.
def intro():
#    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
#    pygame.mixer.music.load("audio/intro.ogg")
#    pygame.mixer.music.play()
    intro = pygame.mixer.Sound('audio/intro.ogg')
    intro.play(1)

def win():
    win = pygame.mixer.Sound('audio/correct.mp3')
    win.play(1)

def lose():
    lose = pygame.mixer.Sound('audio/wrong.mp3')
    lose.play(1)

#To keep our score, we create a variable called score and set it to zero.
score = 0
#The next variable contains the location of the KS2 geography project logo.
logo = "./images/globe.jpg"
#This is a list, sometimes called an array. In here I store two items.
play = ["Yes","No"]

#I start the game by calling the intro() function, and this plays the quiz theme.
intro()
#Here we create a variable called game_start and it will store the answer to the question "Would you like to play the quiz?"
#To capture the answer I use the buttonbox function from easygui. This function has many options, for this I use.
#title = The text at the top of the dialog box.
#image = logo, the variable I earlier created.
#msg = This is the question that I ask the player.
#choices = play. I use this to reference the earlier created list and use the values contained as the choices for the player.
start_title = "Welcome to KS2 Geography Game Quiz"
start_msg = "Would you like to play the Quiz?"
game_start = buttonbox(title=start_title,image=logo,msg=start_msg,choices=play)

#For debugging purposes I have the answer given by the player printed to the Python shell.
print(game_start)#Here we see some conditional logic that tests to see if the answer was "Yes" If the answer is not equal to No, it proceeds.
if game_start != "No":
    #Here is another easygui dialog box, a message box. It has the same syntax as the previous box we created.
    #You can see str(score) in the line below. In order to join a string of text, our message, with the value
    #of the score we need to wrap the score, which is an integer, in a helper function that converts integers
    #and floats into strings
    msgbox(title="Let us begin",msg="Your score is "+str(score))

    count = 0
    #Question 1
    for i in range(0,4):
        msg = "Where is capital of the Netherlands?"
        hint1 = "It's not Tehran"
        hint2 = "It's not London"
        title = "Question 1"
        q1choices = ["Tehran","London","Amsterdam","Abu Dhabi"]
        if count==0:
            q1 = choicebox(msg,title,q1choices)
        elif count ==1:
            msg += hint1
            q1 = choicebox(msg,title,q1choices)
        else:
            msg += hint2
            q1 = choicebox(msg,title,q1choices)

        if q1 is None:
            print("ok, end of game")
            exit()

        if q1 == "Amsterdam":
            win()
            if count == 0:
                score += 1
            elif count ==1:
                score +=0.8
            else:
                score +=0.6
            correct = ("Well done you got it right. Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count = 0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count +=1

    #Question 2
    for i in range(0,4):
        msg = "Which Continent is Britian part of?"
        hint1 = "       You should know this one!"
        hint2 = "       It is the smallest of them all..."
        title = "Question 2"
        q2choices = ["Europe","America", "Asia","Africa"]

        if count == 0:
            q2 = choicebox(msg,title,q2choices)
        elif count ==1:
            msg += hint1
            q2 = choicebox(msg,title,q2choices)
        else:
            msg += hint2
            q2 = choicebox(msg,title,q2choices)

        if q2 == "Europe":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Well done you got it right. Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count =0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count += 1


    #Question 3
    for i in range(0,4):
        msg = "Which of these countries are not in European Union?"
        hint1 = "       located next to Greece!"
        hint2 = "       Capital city of this country called Tirana!"
        title = "Question 3"
        q3choices = ["Latvia","Albania","Estonia","France"]
        if count == 0:
            q3 = choicebox(msg,title,q3choices)
        elif count ==1:
            msg += hint1
            q3 = choicebox(msg,title,q3choices)
        else:
            msg += hint2
            q3 = choicebox(msg,title,q3choices)

        if q3 == "Albania":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Well done you got Albania! hard wasnt it? Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count = 0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer only 3rd Question!"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count += 1


    #Question 4
    for i in range(0,4):
        msg = "How many continents are in the world?"
        hint1 = "       count all of them! "
        hint2 = "       Really? "
        title = "Question 4"
        q4choices = ["7","3","5","4"]

        if count == 0:
            q4 = choicebox(msg,title,q4choices)
        elif count ==1:
            msg += hint1
            q4 = choicebox(msg,title,q4choices)
        else:
            msg += hint2
            q4 = choicebox(msg,title,q4choices)

        if q4 == "7":
            win()
            if count ==0:
                score +=1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Was easy right? Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count =0
            break
        else:
            lose()
            wrong = "nice try! Think again and dont forget to add them all up..."
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1

    #Question 5
    for i in range(0,4):
        msg = "Where is the largest country in Europe?"
        hint1 = "       It is outside EU!"
        hint2 = "       It is also the Largest country in the world!"
        title = "Question 5"
        q5choices = ["France","Germany","Russia","UK"]

        if count ==0:
            q5 = choicebox(msg,title,q5choices)
        elif count ==1:
            msg+=hint1
            q5 = choicebox(msg,title,q5choices)
        else:
            msg+=hint2
            q5 = choicebox(msg,title,q5choices)

        if q5 == "Russia":
            win()
            if count==0:
                score += 1
            elif count ==1:
                score+=0.8
            else:
                score+=0.6

            correct = ("Well done you got it right. Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count=0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1

    #Question 6
    for i in range(0,4):
        msg = "What is a book of maps called?"
        hint1 = "       I Think you pressed the wrong choice by mistake!"
        hint2 = "       Really?"
        title = "Question 6"
        q6choices = ["Dictionary","Book","Atlas","Atlantic"]

        if count ==0:
            q6 = choicebox(msg,title,q6choices)
        elif count ==1:
            msg+=hint1
            q6 = choicebox(msg,title,q6choices)
        else:
            msg+=hint2
            q6 = choicebox(msg,title,q6choices)

        if q6 == "Atlas":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Din not need to think about it right? Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count=0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer! but keep thinking"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1

        #Question 7
    for i in range(0,4):
        msg = "Which is the largest desert in the world?"
        hint1 = "       The area of this desert is 9 400 000 SQ KM"
        hint2 = "       it is located in Africa"
        title = "Question 7"
        q7choices = ["Malavi","Sahara","Gobi","Arabia"]

        if count == 0:
            q7 = choicebox(msg,title,q7choices)
        elif count ==1:
            msg+= hint1
            q7 = choicebox(msg,title,q7choices)
        else:
            msg+=hint2
            q7 = choicebox(msg,title,q7choices)

        if q7 == "Sahara":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("GOOD job mate! hard ones are comimg... Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count=0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1

        #Question 8
    for i in range(0,4):
        msg = "Which is the highest mountain in Britain?"
        hint1 = "       i did not know it myslef so cant help :)"
        hint2 = "       It is located in Scotland somewhere!"
        title = "Question 8"
        q8choices = ["Everest","Mont Blanc","Ben Nevis","Ben Mac"]

        if count==0:
            q8 = choicebox(msg,title,q8choices)
        elif count ==1:
            msg+=hint1
            q8 = choicebox(msg,title,q8choices)
        else:
            msg+=hint2
            q8 = choicebox(msg,title,q8choices)

        if q8 == "Ben Nevis":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Well done you got it right. Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count=0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count += 1

        #Question 9
    for i in range(0,4):
        msg = "When do you see rainbow?"
        hint1 = "       water must be available in air to form a rainbow!"
        hint2 = "       vright light in air plus water will cause this beautiful phenonema!"
        title = "Question 9"
        q9choices = ["When Rainy & Sunny","When Windy & Sunny","When Cloudy & Rainy","When Foggy & Rainy"]

        if count ==0:
            q9 = choicebox(msg,title,q9choices)
        elif count ==1:
            msg+=hint1
            q9 = choicebox(msg,title,q9choices)
        else:
            msg+=hint2
            q9 = choicebox(msg,title,q9choices)

        if q9 == "When Rainy & Sunny":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6

            correct = ("Well done you got it right again... Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count =0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1

        #Question 10
    for i in range(0,4):
        msg = "Which is not a precipitation?"
        hint1 = "       Google it!"
        hint2 = "       it doesnt come from sky!"
        title = "Question 10"
        q10choices = ["Rain","Snow","Hail","Frost"]

        if count ==0:
            q10 = choicebox(msg,title,q10choices)
        elif count ==1:
            msg+=hint1
        else:
            msg+=hint2
            q10 = choicebox(msg,title,q10choices)
        if q10 == "Frost":
            win()
            if count ==0:
                score += 1
            elif count ==1:
                score += 0.8
            else:
                score += 0.6
            score += 1
            correct = ("Well done you got it right. Your score is "+str(score))
            image = "./images/tick.gif"
            msgbox(title="CORRECT",image=image,msg=correct)
            count =0
            break
        else:
            lose()
            wrong = "I'm sorry that's the wrong answer your score is lowering"
            image = "./images/cross.gif"
            msgbox(title="Wrong Answer",image=image,msg=wrong)
            count+=1



    gameover_good = "./images/well_done.gif"
    gameover_bad = "./images/trymore.jpg"
    intro()
    game_over_title = "KS2 Geography Quiz"
    msg_bad = ("Oh dear you scored "+str(score))
    msg_good = ("Well done you scored "+str(score))
    if score < 5:
        game_over = msgbox(title = game_over_title,image = gameover_bad,msg = msg_bad)
    else:
        game_over = msgbox(title = game_over_title,image = gameover_good,msg = msg_good)