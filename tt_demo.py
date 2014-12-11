"""
File for me to learn tk

"""

try:
    import Tkinter as tk
except:
    import tkinter as tk



class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    Singleton decorator class.
    Thank you to Paul Manta http://stackoverflow.com/users/627005/paul-manta
     and stackoverflow
    http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)




@Singleton
class TkinterStorage(object):
    """
    A storage container for all things Tkinter.

    Because it uses the Singleton decorator, it is instantiated only once.
    """
    def __init__(self):
        try:
            import Tkinter as tk
        except:
            import tkinter as tk
        self.tk = tk
        self.root = tk.Tk()

#tk_info = TkinterStorage.Instance()
#w = tk.Label(tk_info.root, text="Hello, world!")
#w.pack()
#tk_info = TkinterStorage.Instance()
#w = tk.Label(tk_info.root, text="I am here")
#w.pack()

#tk_info.root.mainloop()


try:
    from Tkinter import *
except:
    from tkinter import *
import os

class EffbotDialog(Toplevel):
    """
    Nice base class for Dialogs.

    Adapted from the excellent resource: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    """
    def __init__(self, parent, title = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)
    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

class MyDialog(EffbotDialog):
    def body(self, master):
        tk.Label(master, text="Hello, world!").grid(row=0, column=0)
        tk.Label(master, text="foody").grid(row=1, column=1)

#root = tk.Tk()
#MyDialog(root)

#from Tkinter import *

#root = Tk()

def go():
   wdw = Toplevel()
   wdw.geometry('+400+400')
   e = Entry(wdw)
   e.pack()
   e.focus_set()
   wdw.transient(root)
   wdw.grab_set()
   root.wait_window(wdw)
   #print 'done!'

#Button(root, text='Go', command=go).pack()
#Button(root, text='Quit', command=root.destroy).pack()

#root.mainloop()

root = Tk()
root.geometry('+400+400')
l1 = tk.Label(root, text="foody2").grid(row=1, column=1)
root.mainloop()
print("hello")
root = Tk()
root.geometry('+400+400')
l1 = tk.Label(root, text="foody2").grid(row=1, column=1)
root.mainloop()
