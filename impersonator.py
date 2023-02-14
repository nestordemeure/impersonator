"""
Command line interface to interact with personas.
"""

import os

#------------------------------------------------------------------------------
# Utility functions

def _pick_option(picking_message, option_list):
    """
    Given a message describing the choice given
    and a list of string representing potential options
    displays a menu to let the user pick one of the options
    and returns the corresponding string
    """
    result = None
    while result is None:
        # display the list of options
        print(f"\n{picking_message}")
        for i,name in enumerate(option_list):
            print(f"[{i+1}]: {name}")
        # pick one
        user_input = input(f"Please type the name or number of your option of choice: ")
        # validate the user selection
        if user_input in option_list:
            result = user_input
        elif user_input.isdigit():
            i = int(user_input)-1
            if i < len(option_list):
                result = option_list[i]
    return result

#------------------------------------------------------------------------------
# INTRODUCTION

print(f" ===== IMPERSONATOR by Nestor Demeure =====")

# gets the user name for later use
user_name = input(f"\nPlease type your name: ")

# gets the API key if needed
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    print("\nOpenAI API key not found in the 'OPENAI_API_KEY' environement variable")
    print("see this link to obtain an API key: https://platform.openai.com/account/api-keys")
    api_key = input(f"\nPlease type your API key or restart after setting the environement variable: ")
    os.environ['OPENAI_API_KEY'] = api_key

#------------------------------------------------------------------------------
# PERSONA SELECTION

# imported *after* the API key is set
from impersonator import Persona, Chat

print(f"\n ===== Persona selection =====")

# load a persona
persona_picking_message="Please pick one of the folowing persona:"
persona_name = _pick_option(persona_picking_message, Persona.list())
persona = Persona(persona_name)

#------------------------------------------------------------------------------
# CHAT

# display persona and modes picked
print(f"\n ===== Chatting with {persona_name} =====\n")
print("* type FREE to let the persona extrapolate information from now on (the default)")
print("* type STRICT to switch to a somewhat more conservative persona from now on")
print("* type REDO to regenerate the latest answer")
print("* type CHECK to check the last answer against the texts used to generate it")
print("* type SOURCE to display the text extracts used to generate the lastest answer")
print(f"\n ===== Chatting with {persona_name} =====\n")

# initialise the chat
chat = Chat()
last_sources = None

# starts conversation
chat.add_message(persona_name, f"Hi! I am {persona_name}, what can I do for you?", verbose=True)
print()

# runs conversation
while True:
    # get an input from the user
    user_message = input(f"{user_name}: ")
    # process it
    if user_message == 'FREE':
        # switch to non-strict mode
        if persona.is_strict:
            persona.is_strict = False
            print(f"\n> Switched to free mode.\n")
        else:
            print(f"\n> Already in free mode.\n")
    elif user_message == 'STRICT':
        # switch to strict mode
        if persona.is_strict:
            print(f"\n> Already in strict mode.\n")
        else:
            persona.is_strict = True
            print(f"\n> Switched to strict mode.\n")
    elif user_message == 'CHECK':
        # checks last answer against the sources
        last_speaker, last_message = chat.history[-1]
        check = persona.check_answer(last_message, last_sources)
        print(f"\n> {check}\n")
    elif user_message in ["SOURCE", "SOURCES"]:
        # displays the sources
        print(f"\n=========\n{last_sources}\n")
    elif user_message == 'REDO':
        # forgets last message
        chat.history.pop()
        # generates a new message and updates the history with it
        persona_message, sources = persona.chat(user_name, chat.to_string(), sources=last_sources)
        chat.history[-1] = (persona_name, persona_message)
        # displays it
        print()
        chat.add_message(persona_name, persona_message, verbose=True)
        print()
    else:
        # stores the user's message in the chat
        chat.add_message(user_name, user_message, verbose=False)
        # gets an answer from the model
        persona_message, sources = persona.chat(user_name, chat.to_string())
        last_sources = sources
        # displays it
        print()
        chat.add_message(persona_name, persona_message, verbose=True)
        print()
