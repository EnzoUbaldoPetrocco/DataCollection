def accept(text):
    x = input(text)
    # check if there is yes or no
    x = x.lower()
    if x == 'yes' or x =='y':
        return True
    if x == 'no' or x =='n':
        return False
    try:
        x = int(x)
        if x == 1:
            return True
        return False
    except:
        return False
    
def options(options):
    if options == None:
        raise Exception('Options is None')
    if len(options) == 0:
        raise Exception('Options has length 0')
    print('Which one would you like to choose?')
    for i in options:
        print(options)
    x = input('\n')
    for i, option in enumerate(options):
        if x.lower() == option.lower():
            return i + 1
    try:
        x = int(x)
        for i, option in enumerate(options):
            if x == i:
                return i + 1
    except:
        return 0
    return 0