"""Set up a database from documents."""
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

# where is our data?
data_folder = "./data"
# should we split on paragraphs instead of chunking at endlines?
should_split_paragraphs = False
# what is the maximum accepted size for chunks
chunk_size = 1500

# loads the data
print("Loading data...")
loader = DirectoryLoader(data_folder, glob="**/*.docx")
data = loader.load()
print(f"{len(data)} documents loaded.")

# Here we split the documents, as needed, into smaller chunks.
# We do this due to the context limits of the LLMs.
print("Slicing data...")
text_splitter = CharacterTextSplitter(chunk_size=chunk_size, separator="\n")
docs = []
metadatas = []
for i, doc in enumerate(data):
    splits = doc.paragraphs if should_split_paragraphs else text_splitter.split_text(doc.page_content)
    docs.extend(splits)
    metadatas.extend([doc.metadata] * len(splits))
print(f"{len(docs)} slices generated.")

# Creates a vector store from the documents
print("Building embeddings...")
store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)

# saves it to disk
print("Saving...")
store.save_local(folder_path=data_folder)

print("Done.")
