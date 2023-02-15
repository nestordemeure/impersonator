# Impersonator

*Impersonator* lets you chat with an AI simulation of any author, blogger or person as easily as copy-pasting texts they have written into a folder!

## Installation

You will need the following dependencies to run this program:
- `unstructured` (data loading)
- `openai` (models)
- `tiktoken` (tokens counting)
- `bs4` ()
- `langchain` (plumbing)

I recommend creating a [conda](https://docs.conda.io/en/latest/) environment to install all of them.

## Usage

To start the program, put your [OpenAI API key](https://platform.openai.com/account/api-keys) in the environment then start `impersonator.py`.

It will display a list of personas available (see [this page](docs/adding%20a%20persona.md) for ways to add personas).
If you select a persona that has never been used, it will first generate it from the data (which will take time proportional to the amount of data in the `texts` subfolder of your persona).

Once your persona is loaded, you can start chatting with it!

You have a handful of special commands available:
* `CHECK` will run a fact checker on the persona's latest affirmation,
* `SOURCE` will display the text extracts used to synthesize the answer.

## Documentation

* [Guide to adding your own personas](docs/adding%20a%20persona.md)
* [Detailled explanation of the algorithm](docs/inner%20workings.md)

## Potential improvements

* test importation of pdf and format with images

* detail guide to adding a new personna
* update readme with commands

* add a better example persona
  find open example that would be of interest
  (project gutenberg might be a good source? or a blogger's work)
  don giovani?

* Set things up to make it easy to install with pip or similar (if possible include dependencies)
* Suggest for inclusion in [LangChainHub](https://github.com/hwchase17/langchain-hub)

* add the possibility of having multiple persona interacting in a single chatb
* Add a non-shell UI

Do not hesitate to submit pull requests to this repository if you find improvements or good alternative prompts!