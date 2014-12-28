__author__ = 'Robert'

*** Instead maybe use prototype B


from easygui import dynamic as deg

deg.button_box(name='first_bb') # name is the only required argument.  By default, the buttonbox is shown
deg.first_bb.title = "My first sample"

# The following two lines set up the buttons with text and also images.
texts = ["Button[1]", "Button[2]", "Button[3]"]
images = ["...*.jpg", "...", "..."]
deg.first_bb.choices.text = texts
deg.first_bb.choices.image = images

# Or, I could do this:
for i, choice in enumerate(deg.first_bb.choices):
    choice.text = texts[i]
    choice.image = images[i]


