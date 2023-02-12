"""Used to load a personna."""
import os
from pathlib import Path
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

DEFAULT_PERSONAS_FOLDER='./personas'
EMBEDDING_MODEL=OpenAIEmbeddings()
CHUNK_SIZE=1000#100

class Persona:
    """
    Stores all the information about a given persona.
    """

    def list(personas_folder=DEFAULT_PERSONAS_FOLDER):
        """
        returns a list of the names of all personas available
        """
        return [f.name for f in os.scandir(personas_folder) if f.is_dir()]

    def __init__(self, name, personas_folder=DEFAULT_PERSONAS_FOLDER):
        """
        takes the name of a persona and loads it into memory
        generates it if it has not been generated before
        """
        self.name = name 
        self.personas_folder = Path(personas_folder)
        self.persona_path = self.personas_folder / name      
        # loads the vector database
        if self.database_exist():
            self.database = FAISS.load_local(folder_path=self.persona_path, embeddings=EMBEDDING_MODEL)
        else:
            self.database = self.generate_database()
    
    def database_exist(self):
        """
        returns True if the vector database has already been built
        """
        index_faiss = self.persona_path / 'index.faiss'
        index_pkl = self.persona_path / 'index.pkl'
        return index_faiss.is_file() and index_pkl.is_file()

    def generate_database(self):
        """
        builds the vector database from scratch
        saves it in a folder
        returns it
        WARNING: this operation can be slow and costly in OpenAI embeddings costs
        """
        print(f"Generating the vector database for '{self.name}'.")
        documents_path = self.persona_path / 'texts'
        # loading the documents
        loader = DirectoryLoader(documents_path)
        raw_documents = loader.load()
        print(f"   Loaded {len(raw_documents)} documents.")
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

    def similarity_search(self, text, k=4):
        """returns the k closest pieces of text"""
        return self.database.similarity_search(text, k=k)