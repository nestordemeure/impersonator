"""Used to load a personna."""
import os
from pathlib import Path
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from .prompts_models import EMBEDDING_MODEL, embedding_chain, answering_chain, strict_answering_chain, check_chain, writing_chain

DEFAULT_PERSONAS_FOLDER='./personas'
CHUNK_SIZE=1000


class Persona:
    """
    Stores all the information about a given persona.
    """

    def list(personas_folder=DEFAULT_PERSONAS_FOLDER):
        """
        returns a list of the names of all personas available
        """
        return [f.name for f in os.scandir(personas_folder) if f.is_dir()]

    def __init__(self, name, use_strict=False, personas_folder=DEFAULT_PERSONAS_FOLDER):
        """
        takes the name of a persona and loads it into memory
        generates it if it has not been generated before
        """
        # persona information
        self.name = name 
        self.personas_folder = Path(personas_folder)
        self.persona_path = self.personas_folder / name
        self.is_strict = use_strict  
        # documents database
        if self._database_exist():
            self.database = FAISS.load_local(folder_path=self.persona_path, embeddings=EMBEDDING_MODEL)
        else:
            self.database = self._generate_database()
    
    # ----- DATABASE -----

    def _database_exist(self):
        """
        returns True if the vector database has already been built
        """
        index_faiss = self.persona_path / 'index.faiss'
        index_pkl = self.persona_path / 'index.pkl'
        return index_faiss.is_file() and index_pkl.is_file()

    def _generate_database(self):
        """
        builds the vector database from scratch and saves it in a folder
        returns it
        WARNING: this operation can be slow and costly in OpenAI embeddings costs
        """
        print(f"Generating the vector database for '{self.name}'.")
        # loading the documents
        documents_path = self.persona_path / 'texts'
        loader = DirectoryLoader(documents_path)
        raw_documents = loader.load()
        print(f"   Loaded {len(raw_documents)} documents.")
        # labeling documents as being written by the persona or not
        for document in raw_documents:
            in_about_folder = 'texts/about/' in document.metadata['source']
            document.metadata['written_by_persona'] = not in_about_folder
        # splitting the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_SIZE//10)
        documents = text_splitter.split_documents(raw_documents)
        print(f"   Built {len(documents)} text chunks.")
        # building the database
        database = FAISS.from_documents(documents, EMBEDDING_MODEL)
        database.save_local(self.persona_path)
        print(f"   Built vector database.")
        # returning the result
        print(f"   Done.")
        return database

    def get_sources(self, user_name, chat_history, nb_sources=4, separator='=========', verbose=False):
        """gets text extracts that seem relevant to the question"""
        # gets a summary of the themes in the question to help with embedding search
        embeding_text = embedding_chain({'user_name':user_name, 'name':self.name, 'chat_history': chat_history})['text'].strip()
        if verbose: print(f"> Embeding text: {embeding_text}")
        # gets documents to help answer the question
        documents = self.database.similarity_search(embeding_text, k=nb_sources)
        # converts them into a string
        sources = ""
        for doc in documents:
            sources += doc.page_content
            sources += f"\n{separator}\n"
        return sources

    # ----- CHAT -----

    def chat(self, user_name, chat_history, sources=None, nb_sources=4, verbose=False):
        """
        pass a user_name, chat_history (string) and optionaly sources to the persona
        returns a pair (answer, sources)
        """
        # gets sources if needed
        if sources is None:
            sources = self.get_sources(user_name, chat_history, nb_sources, verbose=verbose)
        # gets an answer from the model and returns
        if self.is_strict:
            answer = strict_answering_chain({'name':self.name, 'sources': sources, 'chat_history': chat_history})['text'].strip()
        else:
            answer = answering_chain({'name':self.name, 'sources': sources, 'chat_history': chat_history})['text'].strip()
        return (answer, sources)

    def write(self, user_name, question, sources=None, nb_sources=4, verbose=False):
        """
        get the persona to write a text on a given subject
        returns a long answer
        and the corresponding sources
        """
        # gets sources if needed
        if sources is None:
            sources = self.get_sources(user_name, question, nb_sources, verbose=verbose)
        # gets an answer from the model and returns
        answer = writing_chain({'name':self.name, 'sources': sources, 'specification': question})['text'].strip()
        return (answer, sources)

    def check_answer(self, answer, sources):
        """
        factcheck the chatbot's answer given the corresponding sources
        """
        return check_chain({'name':self.name, 'sources': sources, 'answer':answer})['text'].strip()
