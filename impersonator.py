from impersonator import Persona, Chatbot, Speaker

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

#------------------------------------------------------------------------------
# PERSONA SELECTION

print(f"\n ===== Persona selection =====")

# load a persona
persona_picking_message="Please pick one of the folowing persona:"
persona_name = _pick_option(persona_picking_message, Persona.list())
persona = Persona(persona_name)
persona_modes = []

# pick a strictness mode
strictness_picking_message="Do you want to use Strict Mode?\nIt tries to keep the AI from extrapolating facts from the texts:"
use_strict_mode = _pick_option(strictness_picking_message, ['yes', 'no']) == 'yes'

#------------------------------------------------------------------------------
# CHAT

# display persona and modes picked
mode_string = '(strict)' if use_strict_mode else ''
print(f"\n ===== Chatting with {persona_name} {mode_string} =====")

# initialise the chat
introductory_message = f"Hi! I am {persona_name}, what can I do for you?"
chat = Chatbot(persona, user_name=user_name, chat_history=[(Speaker.Ai,introductory_message )], 
               use_strict_mode=use_strict_mode, verbose=False)

# starts the conversation
print(f"\n{persona_name}: {introductory_message}\n")
while True:
    # gets a question from the user
    question = input(f"{user_name}: ")

    # gets a result from the model
    answer = chat.ask(question)
    print(f"\n{persona_name}: {answer}\n")
