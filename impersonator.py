from impersonator import Persona, Chatbot, Speaker

#------------------------------------------------------------------------------
# INTRODUCTION

print(f" ===== IMPERSONATOR by Nestor Dee =====")

# gets the user name for later use
user_name = input(f"\nPlease type your name: ")

#------------------------------------------------------------------------------
# PERSONA SELECTION

print(f"\n ===== Persona selection =====")

# pick a persona
persona_names =  Persona.list()
persona_name = None
while persona_name is None:
    # display the list of personas
    print("\nPlease pick one of the folowing persona:")
    for i,name in enumerate(persona_names):
        print(f"[{i+1}]: {name}")
    # pick one
    user_input = input(f"Please type the name or number of your persona of choice: ")
    if user_input in persona_names:
        persona_name = user_input
    elif user_input.isdigit():
        i = int(user_input)-1
        if i < len(persona_names):
            persona_name = persona_names[i]

# load the persona
persona = Persona(persona_name)

#------------------------------------------------------------------------------
# CHAT

print(f"\n ===== Chatting with {persona_name} =====")

# initialise the chat
introductory_message = f"Hi! I am {persona_name}, what can I do for you?"
chat = Chatbot(persona, user_name=user_name, chat_history=[(Speaker.Ai,introductory_message )])

# starts the conversation
print(f"\n{persona_name}: {introductory_message}\n")
while True:
    # gets a question from the user
    question = input(f"{user_name}: ")

    # gets a result from the model
    answer = chat.ask(question)
    print(f"\n{persona_name}: {answer}\n")
