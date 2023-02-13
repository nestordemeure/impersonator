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

#------------------------------------------------------------------------------
# CHAT

# display persona and modes picked
print(f"\n ===== Chatting with {persona_name} =====")
print("[type FREE to let the persona extrapolate information from now on (the default)]")
print("[type STRICT to switch to a more conservative persona from now on]")
print("[type CHECK to check the last answer against the texts used to generate it]")
print("[type SOURCE to display the text extracts used to generate the last answer]")

# initialise the chat
introductory_message = f"Hi! I am {persona_name}, what can I do for you?"
chat = Chatbot(persona, user_name=user_name, chat_history=[(Speaker.Ai,introductory_message )], 
               verbose=False)

# starts the conversation
print(f"\n{persona_name}: {introductory_message}\n")
while True:
    # gets a question from the user
    question = input(f"{user_name}: ")
    if question == 'FREE':
        # switch to non-strict mode
        chat.use_strict = False
        print(f"\n> Activated free mode.\n")
    elif question == 'STRICT':
        # switch to strict mode
        chat.use_strict = True
        print(f"\n> Activated strict mode.\n")
    elif question == 'CHECK':
        # checks last answer against the sources
        check = chat.check_last_answer()
        print(f"\n> {check}\n")
    elif question in ["SOURCE", "SOURCES"]:
        # displays the sources
        sources = chat.get_sources()
        print(f"\n{sources}\n")
    else:
        # gets an answer from the model
        answer = chat.ask(question)
        print(f"\n{persona_name}: {answer}\n")
