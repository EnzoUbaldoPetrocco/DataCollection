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
    
def options(options, default=1):
    if options == None:
        raise Exception('Options is None')
    if len(options) == 0:
        raise Exception('Options has length 0')
    print('Which one would you like to choose?')
    for i, opt in enumerate(options):
        print(f'{i+1}) {opt}')
    x = input('')
    for i, option in enumerate(options):
        if x.lower() == option.lower():
            return i + 1
    try:
        x = int(x)
        if x >= 1 and x <= len(options):
            return x
        else:
            return default
    except:
        return default