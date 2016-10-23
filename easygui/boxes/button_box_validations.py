
# Validation of images

def validate_images(image, images):
    """
    Validates input and converts it into a fixed type (a list of lists)
    """
    imgs = _check_images_parameter(image, images)
    images = _images_to_matrix(imgs)
    return images


def _check_images_parameter(image, images):
    """ parameter image is deprecated, here we deal with it"""
    if image and images:
        raise ValueError("Specify 'images' parameter only for buttonbox.")
    if image:
        images = image
    return images


def _images_to_matrix(img_file_names):
    """
    Transform img_file_names, into a list of lists of filenames
    Also check that the file names are strings.
    :param img_file_names:
    May be a file name (which will generate a single image), a list of file names (which will generate
    a row of images), or a list of list of filename (which will create a 2D array of buttons.
    :return: img_as_matrix
    A list of lists of strings
    """

    if img_file_names is None:
        return None

    # Convert to a list of lists of file_names regardless of input
    if _is_string(img_file_names):
        img_as_matrix = [[img_file_names, ], ]
    elif _is_sequence(img_file_names) and _is_string(img_file_names[0]):
        img_as_matrix = [img_file_names, ]
    elif _is_sequence(img_file_names) and _is_sequence(img_file_names[0]) and _is_string(img_file_names[0][0]):
        img_as_matrix = img_file_names
    else:
        raise ValueError("Incorrect images argument.")

    return img_as_matrix


def _is_sequence(something):
    """ Check if something is a list or tuple, but not string"""
    # REF: http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string

    return hasattr(something, "__getitem__") or hasattr(something, "__iter__")


# Validation of the msg -------------------------------------------------------------

def validate_msg(something):
    """
    Make sure msg is a string, if not try hard to turn it into a string
    """

    if _is_string(something):
        return something

    try:
        text = "".join(something)  # convert a list or a tuple to a string
    except:
        err_msg = "Exception when trying to convert {}, which is type {} to text".format(something, type(something))
        raise ValueError(err_msg)
    return text


# Used by both  ---------------------------------------

def _is_string(something):
    """ Check if something is a string"""
    try:
        ret_val = isinstance(something, basestring) #Python 2
    except:
        ret_val = isinstance(something, str) #Python 3
    return ret_val

