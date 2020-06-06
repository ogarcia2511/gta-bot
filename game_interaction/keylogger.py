import win32api

# list of keys to listen for
lst = ['W', 'A', 'S', 'D']

def get():
    keys = []
    for key in lst:
        if win32api.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
