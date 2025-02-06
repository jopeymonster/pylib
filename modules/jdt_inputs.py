# custom_inputs by Joe Thompson, 2024

import sys

"""
Function version
"""

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


"""
Alternate function not overriding '__builtins__'
"""
def custom_input(prompt=''):
    user_input = input(prompt)
    if user_input.lower() == 'ex':
        print("Exiting the program.")
        sys.exit()
    return user_input

# Example usage:
while True:
    user_input = custom_input("Enter 1 or 2 ('ex' to exit): ")
    if user_input in ["1","2"]:
        print(f"You entered: {user_input}")
    else:
        print("Thank you!")
        break

"""
Class version using context manager
"""
import sys

class OverrideInput:
    def __init__(self, exit_keyword="ex"):
        self.exit_keyword = exit_keyword
        self.original_input = __builtins__.input

    def __enter__(self):
        __builtins__.input = self.custom_input

    def __exit__(self, exc_type, exc_val, exc_tb):
        __builtins__.input = self.original_input

    def custom_input(self, prompt=''):
        user_input = self.original_input(prompt)
        if user_input.lower() == self.exit_keyword:
            print("Exiting the program.")
            sys.exit()
        return user_input

# Example usage:
with OverrideInput(exit_keyword="ex"):
    while True:
        user_input = input("Enter something ('ex' to exit): ")
        print(f"You entered: {user_input}")

