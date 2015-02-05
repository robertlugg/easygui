"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os
import pickle


# -----------------------------------------------------------------------
#
#     class EgStore
#
# -----------------------------------------------------------------------
class EgStore:

    r"""
A class to support persistent storage.

You can use EgStore to support the storage and retrieval
of user settings for an EasyGui application.

**Example A: define a class named Settings as a subclass of EgStore**
::

    class Settings(EgStore):
        def __init__(self, filename):  # filename is required
            #-------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            #-------------------------------------------------
            self.userId = ""
            self.targetServer = ""

            #-------------------------------------------------
            # For subclasses of EgStore, these must be
            # the last two statements in  __init__
            #-------------------------------------------------
            self.filename = filename  # this is required
            self.restore()            # restore values from the storage file if possible

**Example B: create settings, a persistent Settings object**
::

    settingsFile = "myApp_settings.txt"
    settings = Settings(settingsFile)

    user    = "obama_barak"
    server  = "whitehouse1"
    settings.userId = user
    settings.targetServer = server
    settings.store()    # persist the settings

    # run code that gets a new value for userId, and persist the settings
    user    = "biden_joe"
    settings.userId = user
    settings.store()

**Example C: recover the Settings instance, change an attribute, and store it again.**
::

    settings = Settings(settingsFile)
    settings.userId = "vanrossum_g"
    settings.store()

"""

    def __init__(self, filename):  # obtaining filename is required
        self.filename = None
        raise NotImplementedError()

    def restore(self):
        """
        Set the values of whatever attributes are recoverable
        from the pickle file.

        Populate the attributes (the __dict__) of the EgStore object
        from     the attributes (the __dict__) of the pickled object.

        If the pickled object has attributes that have been initialized
        in the EgStore object, then those attributes of the EgStore object
        will be replaced by the values of the corresponding attributes
        in the pickled object.

        If the pickled object is missing some attributes that have
        been initialized in the EgStore object, then those attributes
        of the EgStore object will retain the values that they were
        initialized with.

        If the pickled object has some attributes that were not
        initialized in the EgStore object, then those attributes
        will be ignored.

        IN SUMMARY:

        After the recover() operation, the EgStore object will have all,
        and only, the attributes that it had when it was initialized.

        Where possible, those attributes will have values recovered
        from the pickled object.
        """
        if not os.path.exists(self.filename):
            return self
        if not os.path.isfile(self.filename):
            return self

        try:
            with open(self.filename, "rb") as f:
                unpickledObject = pickle.load(f)

            for key in list(self.__dict__.keys()):
                default = self.__dict__[key]
                self.__dict__[key] = unpickledObject.__dict__.get(key, default)
        except:
            pass

        return self

    def store(self):
        """
        Save the attributes of the EgStore object to a pickle file.
        Note that if the directory for the pickle file does not already exist,
        the store operation will fail.
        """
        with open(self.filename, "wb") as f:
            pickle.dump(self, f)

    def kill(self):
        """
        Delete my persistent file (i.e. pickle file), if it exists.
        """
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        return

    def __str__(self):
        """
        return my contents as a string in an easy-to-read format.
        """
        # find the length of the longest attribute name
        longest_key_length = 0
        keys = list()
        for key in self.__dict__.keys():
            keys.append(key)
            longest_key_length = max(longest_key_length, len(key))

        keys.sort()  # sort the attribute names
        lines = list()
        for key in keys:
            value = self.__dict__[key]
            key = key.ljust(longest_key_length)
            lines.append("%s : %s\n" % (key, repr(value)))
        return "".join(lines)  # return a string showing the attributes
