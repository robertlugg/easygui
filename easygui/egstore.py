"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""
import errno
import os
import pickle
import datetime

def read_or_create_settings(file_name):
    settings = Settings(file_name)
    settings.restore()
    return settings

class EgStore(object):
    """
    A class to support persistent storage.

    You can use ``EgStore`` to support the storage and retrieval
    of user settings for an EasyGui application.

    **First: define a class named Settings as a subclass of EgStore** ::

        class Settings(EgStore):
            def __init__(self, filename):  # filename is required
                # specify default values for variables that this application wants to remember
                self.user_id = ''
                self.target_server = ''
                settings.restore()
    *Second: create a persistent Settings object** ::

        settings = Settings('app_settings.txt')
        settings.user_id = 'obama_barak'
        settings.targetServer = 'whitehouse1'
        settings.store()

        # run code that gets a new value for user_id, and persist the settings
        settings.user_id = 'biden_joe'
        settings.store()

    **Example C: recover the Settings instance, change an attribute, and store it again.** ::

        settings = Settings('app_settings.txt')
        settings.restore()
        print settings
        settings.user_id = 'vanrossum_g'
        settings.store()
    """

    def __init__(self, filename):
        """Initialize a store with the given filename.

        :param filename: the file that backs this store for saving and loading
        """

        self.filename = filename

    def restore(self):
        try:
            self._restore()
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise


    def _restore(self):
        """
        Set the values of whatever attributes are recoverable
        from the pickle file.

        Populate the attributes (the __dict__) of the EgStore object
        from the attributes (the __dict__) of the pickled object.

        If the pickled object has attributes that have been initialized
        in the EgStore object, then those attributes of the EgStore object
        will be replaced by the values of the corresponding attributes
        in the pickled object.

        If the pickled object is missing some attributes that have
        been initialized in the EgStore object, then those attributes
        of the EgStore object will retain the values that they were
        initialized with.

        Where possible, the attributes will have values recovered
        from the pickled object.
        """
        with open(self.filename, 'rb') as f:
            store = pickle.load(f)

        for key, value in store.__dict__.items():
            self.__dict__[key] = value

        self.last_time_restored = datetime.datetime.now()


    def store(self):
        """Save this store to a pickle file.
        All directories in :attr:`filename` must already exist.
        """

        with open(self.filename, 'wb') as f:
            self.last_time_stored = datetime.datetime.now()
            pickle.dump(self, f)


    def kill(self):
        """Delete this store's file if it exists."""

        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def __getstate__(self):
        """ All attributes will be pickled """
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """ Ensure filename won't be unpickled """
        if 'filename' in state:
            del state['filename']
        self.__dict__.update(state)

    def __str__(self):
        """"Format this store as "key : value" pairs, one per line."""
        stored_values = self.__dict__
        lines = []
        width = max(len(key) for key in stored_values)
        for key in sorted(stored_values.keys()):
            value = stored_values[key]
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            lines.append('{0} : {1!r}'.format(key.ljust(width), value))
        return '\n'.join(lines)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


class Settings(EgStore):
    def __init__(self, filename):
        self.filename = filename
