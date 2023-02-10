from enum import Enum
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

#----------------------------------------------------------------------------------------
# String conversion

class Speaker(Enum):
    """enum to represent the speaker"""
    Ai = 0
    Human = 1

def _context_to_string(documents):
    """
    turns a list of strings used for context into a string
    """
    result = ""
    for doc in documents:
        result += doc.page_content
        result += '\n=========\n'
    return result

def _chat_to_string(chat_history, human_name, ai_name, max_messages):
    """
    turns the last max_messages messages in the chat_history into a string
    """
    result = ""
    # truncate the chat history
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]
        result += "..."
    # assembles the chat
    for (speaker,message) in chat_history:
        speaker = ai_name if (speaker == Speaker.Ai) else human_name
        message = f"{speaker}: {message}\n"
        result += message
    return result

#----------------------------------------------------------------------------------------
# Model and prompt

# the language model that will be used
LANGUAGE_MODEL = OpenAI(temperature=0.7)

# prompt to answer the question
template = """You are {name} and are answering questions.
You are given the following extracts of texts you have written and the latest messages in the conversation.
Provide a conversational answer. Stay close to the style and voice of your texts.

EXTRACTS:
{extracts}

CHAT:
{chat_history}
{name}:"""
PROMPT = PromptTemplate.from_template(template)

#----------------------------------------------------------------------------------------
# Chat

class Chatbot:
    """Represents a chatbot and chat with a given persona"""
    def __init__(self, persona, user_name, chat_history=[], max_chat_size=10):
        self.user_name = user_name
        self.persona = persona
        self.chat_history = chat_history
        self.max_chat_size = max_chat_size
        self.chain = LLMChain(llm=LANGUAGE_MODEL, prompt=PROMPT, verbose=False)

    def ask(self, question):
        """
        ask a question to the chatbot
        returns an answer
        """
        self.chat_history.append((Speaker.Human, question))
        # gets extracts of text to help answer the question
        extracts = self.persona.similarity_search(question)
        extracts = _context_to_string(extracts)
        # gets the chat history
        chat_history = _chat_to_string(self.chat_history, self.user_name, self.persona.name, self.max_chat_size)
        # gets an answer rom the model
        answer = self.chain({'name':self.persona.name, 'extracts': extracts, 'chat_history': chat_history})['text'].strip()
        # save and return
        self.chat_history.append((Speaker.Ai, answer))
        return answer
