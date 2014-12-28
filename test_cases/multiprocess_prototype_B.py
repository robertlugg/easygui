    __author__ = 'Robert'

    import sys

    sys.path.append('..')
    import easygui as eg

    ###############################
    print "The next three examples all do the same thing.  I gave all three just to show" \
          "what the code would look like"

    # This works just like before
    reply = eg.buttonbox()  # This blocks until the user presses a button or closes the window.
    print reply

    # *** This is the new stuff ***

    #The following works just like the "old-style" sample above:
    reply = eg.buttonbox(name='my_box1', run=True)
    print reply

    # The following creates a buttonbox just like the default one above.  It is shown, but does not block (ie returns
    # immediately)
    eg.buttonbox(name='my_box1', run=False)
    print "The GUI has appeared but is disabled"
    reply = eg.my_box1.run()  # Now, the GUI is enabled.  This blocks until the user presses or closes the window
    print reply
    ###############################

    print "This example shows how I would setup the buttons myself and put text and images in them"

    eg.buttonbox(name='my_box2', run=False)
    eg.my_box2.choices = ['Yes', 'No', 'Maybe', "I don't care"]  # Change to have four buttons
    eg.my_box2.choices[3].enabled = False  # Disable fourth option
    eg.my_box2.choices.images = ['check.jpg', 'x.jpg', 'question.jpg', 'XXXX.jpg']
    eg.my_box2.choices[0].text = "Yup"
    eg.my_box2.choices[1].text = "Nope"
    eg.my_box2.message = "Start pressing buttons!!!!"
    eg.timeout = 60  # Timeout after 60 seconds
    eg_timeout_return_value = None  # If timeout is reached, return this value

    press_count = 0
    while True:
        reply = eg.my_box2.run()
        if reply is None:
            break
        press_count += 1
        eg.my_box2.message = "You have pressed a button {0} time(s)".format(press_count)
        print reply


