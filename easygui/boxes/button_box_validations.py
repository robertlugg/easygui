import collections
import sys

try:
    from .text_box import textbox
except (SystemError, ValueError, ImportError):
    from text_box import textbox


class Validations(object):
    """ All validations and tranformations to user input
        before feeding data to ui
    """

    def validate_images(self, image, images):
        """ parameter image is deprecated, here we deal with it"""
        if image and images:
            raise ValueError("Specify 'images' parameter only for buttonbox.")
        if image:
            images = image
        return images

    def images_to_matrix(self, img_filenames):
        """
        Transform img_filenames, into a list of lists of filenames
        Also check that the filenames are strings.
        :param img_filenames:
        May be a filename (which will generate a single image), a list of filenames (which will generate
        a row of images), or a list of list of filename (which will create a 2D array of buttons.
        :return: img_as_matrix
        A list of lists of strings
        """

        if img_filenames is None:
            return
        # Convert to a list of lists of filenames regardless of input
        if self.is_string(img_filenames):
            img_as_matrix = [[img_filenames, ], ]
        elif self.is_sequence(img_filenames) and self.is_string(img_filenames[0]):
            img_as_matrix = [img_filenames, ]
        elif self.is_sequence(img_filenames) and self.is_sequence(img_filenames[0]) and self.is_string(img_filenames[0][0]):
            pass
        else:
            raise ValueError("Incorrect images argument.")

        return img_as_matrix

    def convert_choices_to_dict(self, choices):
        """
        User can enter choices as a single string, a list of strings and a dictionary
        Here we transform them all into a dicrionary
        """
        if isinstance(choices, collections.Mapping): # If it is dictionary-like
            choices_dict = choices
        else:
            # Convert into a dictionary of equal key and values
            choices_list = list(choices)
            choices_dict = {i: i for i in choices_list}
        return choices_dict

    def validate_msg(self, msg):
        """ Make sure msg is a string
        """
        return self.to_string(msg)

    def to_string(self, something):
        """ Try hard to turn something into a string"""
        try:
            basestring  # python 2
        except NameError:
            basestring = str  # Python 3

        if isinstance(something, basestring):
            return something
        try:
            text = "".join(something)  # convert a list or a tuple to a string
        except:
            err_msg = "Exception when trying to convert {}, which is fo type {} to text".format(something, type(something))
            print(err_msg)
            textbox(err_msg)
            raise
        return text

    # REF: http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
    def is_sequence(self, something):
        """ Check if something is a list or tuple, but not string"""
        return hasattr(something, "__getitem__") or hasattr(something, "__iter__")


    def is_string(self, something):
        """ Check if something is a string"""
        ret_val = None
        try:
            ret_val = isinstance(something, basestring) #Python 2
        except:
            ret_val = isinstance(something, str) #Python 3
        return ret_val