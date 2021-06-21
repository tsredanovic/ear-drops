def manually_set_value(field, default_value=None):
    if default_value:
        print('{}: {}'.format(field.capitalize(), default_value))
        if confirm(field):
            return default_value

    while True:
        value = input('{}: '.format(field.capitalize()))
        if confirm(field):
            break

    return value

def confirm(field):
    confirmation = input('{} correct?(y/n)'.format(field.capitalize()))
    if confirmation in ['y', 'yes']:
        return True
    else:
        return False
