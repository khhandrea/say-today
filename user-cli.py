import sys
import requests

def sayings_get():
    global url
    res = requests.get(f'{url}/sayings')
    return res.json()['message']

def sayings_post(saying):
    global url
    data = {'saying': saying}
    res = requests.post(
        f'{url}/sayings',
        json=data)
    print(f'upload succefully with status code {res.status_code}.')

if __name__ == '__main__':
    url = 'localhost:5000'
    if len(sys.argv) == 2:
        url = sys.argv[1]
        
    while True:
        print('hello! say me anything : ', end='')
        user_input = input()

        if user_input == 'help':
            print('1. sayings-get : get a random saying')
            print('2. sayings-post [saying] : post a saying')
        elif user_input == 'get':
            print(sayings_get())
        elif user_input.split()[0] == ('post'):
            if len(user_input.split()) > 1:
                sayings_post(' '.join(user_input.split()[1:]))
            else:
                print('need argument')
        elif user_input == 'exit':
            print('bye')
            break
        else:
            print('command not found')