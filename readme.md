# Impersonator

*Impersonator* lets you chat with an AI simulation of any author, blogger or person as easily as copy-pasting texts they have written into a folder!

See [this page of the documentation](docs/inner%20workings.md) for a detailled explanation of the algorithm.

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

You have a handful of special commands available:
* `CHECK` will run a fact checker on the persona's latest affirmation,
* `SOURCE` will display the text extracts used to synthesize the answer.

#### Adding a persona

To add a persona, add a subfolder in the `personas` folder.

Your subfolder should:
- be named like your persona (i.e. `John Doe`)
- include texts written by them (if possible non-fiction, correspondence would be best) in a `texts` subfolder (common formats such as `.txt`, `.html`, `.docx` should work fine, you might have to convert other formats).

To reload a persona from scratch (taking into account new files), delete the `index.faiss` and `index.pkl` files in its folder.

See the `John Doe` folder for a small example.

See [this page of the documentation](docs/adding%20a%20persona.md) for a detailled guide to add new personas to the application.

## Inner-Workings

When a persona is created, its texts are split into chunks that are stored in a [vector database](https://www.pinecone.io/learn/vector-database/) for easy retrieval.

When you talk to a persona, it receives the following prompt (containing the recent history of the chat as well as text chunks that seem relevant to the conversation):

```
You are {name} and are answering questions.
You are given the following extracts of texts you have written and the latest messages in the conversation.
Provide a conversational answer. Stay close to the style and voice of your texts.

EXTRACTS:
{extracts}

CHAT:
{chat_history}
{name}:
```

The AI (currently [GPT-3](https://en.wikipedia.org/wiki/GPT-3)) then synthesizes a likely answer from the information it is given, pushing the conversation to the next message (here the ability of the AI to both hallucinate information and pick up on style is helpful to strengthen the illusion).

## Potential improvements

* test importation of pdf and format with images

* write guide to adding a new personna
* update the inner-workings guide as well as the readme to note that strict is being used

* add a better example persona
  find open example that would be of interest
  (project gutenberg might be a good source? or a blogger's work)
  don giovani?

* Set things up to make it easy to install with pip or similar (if possible include dependencies)
* Suggest for inclusion in [LangChainHub](https://github.com/hwchase17/langchain-hub)

* add an option to ask a single question and get a long answer (with REDO)
* add the possibility of having multiple persona interacting in a single chatb
* Add a non-shell UI

Do not hesitate to submit pull requests to this repository if you find improvements or good alternative prompts!