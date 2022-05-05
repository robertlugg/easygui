from easygui import multenterbox


def demo1():
    msg = "Enter your personal information"
    title = "Credit Card Application"
    fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
    fieldValues = []  # we start with blanks for the values

    # make sure that none of the fields was left blank
    while True:

        fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
        cancelled = fieldValues is None
        errors = []
        if cancelled:
            pass
        else:  # check for errors
            for name, value in zip(fieldNames, fieldValues):
                if value.strip() == "":
                    errors.append('"{}" is a required field.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            break  # no problems found

        msg = "\n".join(errors)

    print("Reply was: {}".format(fieldValues))


class Demo2():

    def __init__(self):
        msg = "Without flicker. Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
        fieldValues = []  # we start with blanks for the values

        fieldValues = multenterbox(msg, title, fieldNames, fieldValues,
                                   callback=self.check_for_blank_fields)
        print("Reply was: {}".format(fieldValues))

    def check_for_blank_fields(self, box):
        # make sure that none of the fields was left blank
        cancelled = box.return_value is None
        errors = []
        if cancelled:
            pass
        else:  # check for errors
            for name, value in zip(box.fields, box.return_value):
                if value.strip() == "":
                    errors.append('"{}" is a required field.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            box.stop()  # no problems found

        box.msg = "\n".join(errors)


if __name__ == '__main__':
    demo1()
    Demo2()