"""
Command line interface to interact with personas.
"""

import os

#------------------------------------------------------------------------------
# CHAT UI

def chat_ui(persona, user_name):
    """loop on chatting with a persona"""
    # imported *after* the API key is set
    from impersonator import Chat

    # display persona and modes picked
    print(f"\n ===== Chatting with {persona.name} =====\n")
    print("* type FREE to let the persona extrapolate information from now on (the default)")
    print("* type STRICT to switch to a somewhat more conservative persona from now on")
    print("* type REDO to regenerate the latest answer")
    print("* type CHECK to check the last answer against the texts used to generate it")
    print("* type SOURCE to display the text extracts used to generate the lastest answer")
    print("* type EXIT to exit the chat")
    print(f"\n ===== Chatting with {persona.name} =====\n")

    # initialise the chat
    chat = Chat()
    last_sources = None

    # starts conversation
    chat.add_message(persona.name, f"Hi! I am {persona.name}, what can I do for you?", verbose=True)
    print()

    # runs conversation
    while True:
        # get an input from the user
        user_message = input(f"{user_name}: ")
        # process it
        if user_message == 'EXIT':
            # end the chat
            return
        elif user_message == 'FREE':
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
            print(f"\n{last_sources}\n")
        elif user_message == 'REDO':
            # forgets last message
            chat.history.pop()
            # generates a new message and updates the history with it
            persona_message, sources = persona.chat(user_name, chat.to_string(), sources=last_sources)
            chat.history[-1] = (persona.name, persona_message)
            # displays it
            print()
            chat.add_message(persona.name, persona_message, verbose=True)
            print()
        else:
            # stores the user's message in the chat
            chat.add_message(user_name, user_message, verbose=False)
            # gets an answer from the model
            persona_message, sources = persona.chat(user_name, chat.to_string())
            last_sources = sources
            # displays it
            print()
            chat.add_message(persona.name, persona_message, verbose=True)
            print()

#------------------------------------------------------------------------------
# PERSONA SELECTION UI

def persona_selection_ui(user_name):
    """loop on picking a persona and chatting with it"""
    # imported *after* the API key is set
    from impersonator import Persona

    # runs conversation
    while True:
        print(f"\n ===== Persona selection =====")

        # pick a persona
        persona_list = Persona.list()
        persona_name = None
        while persona_name is None:
            # display the list of options
            print("\nPlease pick one of the folowing persona:")
            for i,name in enumerate(persona_list):
                print(f"[{i+1}]: {name}")
            # pick one
            user_input = input("Please type the name or number of your option of choice (type EXIT to kill the program): ")
            # validate the user selection
            if user_input == 'EXIT':
                # end the program
                return
            elif user_input in persona_list:
                # persona is a known name
                persona_name = user_input
            elif user_input.isdigit():
                # persona is a number
                i = int(user_input)-1
                if i < len(persona_list):
                    persona_name = persona_list[i]

        # load the persona
        persona = Persona(persona_name)

        # starts a chat
        chat_ui(persona, user_name)

#------------------------------------------------------------------------------
# MAIN UI

def main_ui():
    """main user interface"""
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
    
    # starts the persona selection
    persona_selection_ui(user_name)

    # Done!
    print("\nGood bye!")

#------------------------------------------------------------------------------
# MAIN

main_ui()