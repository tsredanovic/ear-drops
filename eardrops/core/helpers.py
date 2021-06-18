def manually_set_value(value):
    while True:
        value = input('{}: '.format(value.capitalize()))

        confirmation = input('We Happy: ')
        if confirmation in ['y', 'yes']:
            break

    return value
