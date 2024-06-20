# custom_inputs by Joe Thompson, 2024

import sys

# exit menu, 'ex'
def custom_input(prompt=''):
    user_input = original_input(prompt)
    if user_input.lower() == 'ex':
        print("Exiting the program.")
        sys.exit()
    return user_input

# set __builtins__ module or a dictionary
if isinstance(__builtins__, dict):
    original_input = __builtins__['input']
    __builtins__['input'] = custom_input
else:
    original_input = __builtins__.input
    __builtins__.input = custom_input
