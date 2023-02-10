
"""Ask a question to the database."""
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain import OpenAI, VectorDBQA

# where is our data?
data_folder = "./data"

# loads the vector store
store = FAISS.load_local(folder_path=data_folder, embeddings=OpenAIEmbeddings())

# builds a Q&A model
model = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=store)
model.return_source_documents = True

def format_sources(sources):
    """returns a set of cleaned-up sources"""
    def doc2source(doc):
        source = doc.metadata['source'] # gets source
        source = source.rpartition('/')[-1] or source # split on last /
        source = source.replace(' ', '~') # replace spaces
        return source
    return {doc2source(doc) for doc in result['source_documents']}

print("===== Ask Questions to Nestor Dee's Notebooks ===\n")
while True:
    # gets a question from the user
    question = input("Question: ")

    # gets a result from the model
    result = model(question)

    # display it with its sources
    print()
    print(f"Answer:{result['result']}\n")
    print(f"Sources: { format_sources(result['source_documents']) }\n")