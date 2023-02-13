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

# prompt to answer the question
template = """You are {name} and are answering questions.
You are given the following extracts of texts you have written and the latest messages in the conversation.
Provide a conversational answer. Stay close to the style and voice of your texts.

EXTRACTS:
{extracts}

CHAT:
{chat_history}
{name}:"""
PROMPT_ANSWER = PromptTemplate.from_template(template)

# prompt to answer the question
# this variant is mostly succesful at forbidding halucinations
template = """You are {name} and are having a sourced conversation.
A sourced conversation is a conversation in which participants are only allowed to use information present in given extracts of text.
You are given the following extracts of texts you have written and the latest messages in the conversation.
Provide a conversational answer. Stay close to the style and voice of your texts.
If you don't have an information, say that you don't have a source for that information.

EXTRACTS:
{extracts}

CHAT:
{chat_history}
{name}:"""
PROMPT_ANSWER_REDUCED_HALUCINATIONS = PromptTemplate.from_template(template)

# prompt to provide a list of topics to search instead of the question when doing similarity search
# this is somewhat inspired by: https://arxiv.org/abs/2212.10496
template = """The following chat ends on a question by {user_name}.
Write a list of queries to google the answer to {user_name}'s last question.
Use precise words, don't be afraid of using synonyms.

CHAT:
{chat_history}

GOOGLE: {name}"""
PROMPT_EMBEDDING = PromptTemplate.from_template(template)

# prompt to fact check the bot's last answer
template = """The following texts have been written by {name}.

SOURCES:
{extracts}

ASSERTION:
{name}: {answer}

The sources are all true.
Determine whether the assertion is true or false. If it is false, explain why."""
PROMPT_CHECK = PromptTemplate.from_template(template)

#----------------------------------------------------------------------------------------
# Chat

class Chatbot:
    """Represents a chatbot and chat with a given persona"""
    def __init__(self, persona, user_name, chat_history=[], max_chat_size=10, verbose=False):
        self.user_name = user_name
        self.persona = persona
        self.chat_history = chat_history
        self.max_chat_size = max_chat_size
        self.verbose = verbose
        self.previous_extracts = ""
        # models
        self.answering_chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=PROMPT_ANSWER, verbose=verbose)
        self.embedding_chain = LLMChain(llm=OpenAI(temperature=0), prompt=PROMPT_EMBEDDING, verbose=verbose)
        self.check_chain = LLMChain(llm=OpenAI(temperature=0), prompt=PROMPT_CHECK, verbose=verbose)

    def ask(self, question):
        """
        ask a question to the chatbot
        returns an answer
        """
        # gets the chat history
        self.chat_history.append((Speaker.Human, question))
        chat_history = _chat_to_string(self.chat_history, self.user_name, self.persona.name, self.max_chat_size)
        # gets a summary of the themes in the question to help with embedding search
        embeding_text = self.embedding_chain({'user_name':self.user_name, 'name':self.persona.name, 'chat_history': chat_history})['text'].strip()
        if self.verbose: print(f"> {embeding_text}")
        # gets extracts of text to help answer the question
        extracts = self.persona.similarity_search(embeding_text)
        extracts = _context_to_string(extracts)
        # gets an answer rom the model
        answer = self.answering_chain({'name':self.persona.name, 'extracts': extracts, 'chat_history': chat_history})['text'].strip()
        # save and return
        self.previous_extracts = extracts
        self.chat_history.append((Speaker.Ai, answer))
        return answer
    
    def get_sources(self):
        """
        returns the sources used to produce the latest affirmation.
        """
        if self.verbose: print("> Fetching sources.")
        return f"=========\n{self.previous_extracts}"

    def check_last_answer(self):
        """
        fact check the chatbot's last answer given the sources
        """
        if self.verbose: print("> Checking answer.")
        # gets the bot lastest affirmation
        answer = self.chat_history[-1][1]
        # checks it
        check = self.check_chain({'name':self.persona.name, 'extracts': self.previous_extracts, 'answer':answer})['text'].strip()
        return check