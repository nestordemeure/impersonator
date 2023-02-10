# Impersonator

*Impersonator* lets you chat with an AI simulation of any author, blogger or person as easily as copy-pasting texts they have written into a folder!

## Usage

#### Installation

You will need the following dependencies to run this program:
- `unstructured` (data loading)
- `openai` (models)
- `tiktoken` (tokens counting)
- `langchain` (plumbing)

I recommend creating a [conda](https://docs.conda.io/en/latest/) environment to install all of them.

#### Using existing personas

To start the program, put your [OpenAI API key](https://openai.com/blog/openai-api/) in the environment then start `impersonator.py`.

It will display a list of personas available (see the next section for ways to add personas).
If you select a persona that has never been used, it will first generate it from the data (which will take time proportional to the amount of data in the `texts` subfolder of your persona).

Once your persona is loaded, you can start chatting with it!

#### Adding a persona

To add a persona, add a subfolder in the `personas` folder.

Your subfolder should:
- be named like your persona (i.e. `John Doe`)
- include a short description of your persona in a `description.txt` file
- include texts written by them (if possible non-fiction, correspondence would be best) in a `texts` subfolder (most common formats such as `.txt`, `.docx` and `.pdf` will work fine).

See the `John Doe` folder for a small example.

## Theory

When a persona is created, its texts are split into chunks that are stored in a [vector database](https://www.pinecone.io/learn/vector-database/).

When you talk to it, it receives the following prompts (containing the recent history of the chat as well as text chunks that seem relevant to the conversation):

```
TODO
```

The AI (currently [GPT-3](https://en.wikipedia.org/wiki/GPT-3)) then synthesizes a likely answer from the information it is given, pushing the conversation to the next message.

This repository is built on top of [LangChain](https://github.com/hwchase17/langchain).

## Potential improvements

* Update `.gitignore` to avoid saving non-example personas
* Set things up to make it easy to install with pip or similar (if possible include dependencies)
* Add a non-shell UI
* suggest for inclusion in [LangChainHub](https://github.com/hwchase17/langchain-hub)
