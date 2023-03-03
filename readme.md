# Impersonator

*Impersonator* lets you chat with an AI simulation of any author, blogger or person as easily as copy-pasting texts they have written into a folder!

## Installation

You will need the following dependencies to run this program:
- `unstructured` (data loading)
- `openai` (models)
- `tiktoken` (tokens counting)
- `bs4` (webpages scraping)
- `langchain` (plumbing)

`faiss-cpu`

`nltk` might require some image recognition models to be installed

I recommend instaling [conda](https://docs.conda.io/en/latest/) and [creating an environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments) as follows to download them:

```
conda env create -f environment.yml
```

Version numbers have been frozen but this program will likely run with newer versions.

## Usage

#### Starting Impersonator

Afterward, you can [activate the environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) whenever you want to use impersonator:

```
conda activate impersonator
```

#### Loading a persona

To start the program, put your [OpenAI API key](https://platform.openai.com/account/api-keys) in the environment then start `impersonator.py`.

It will display a list of personas available (see [this page](docs/adding%20a%20persona.md) for ways to add personas).
If you select a persona that has never been used, it will first generate it from the data (which will take time proportional to the amount of data in the `texts` subfolder of your persona).

Once your persona is loaded, you can start chatting with it!

#### Commands

You have a handful of special commands available:
* `CHECK` will run a fact checker on the persona's latest affirmation,
* `SOURCE` will display the text extracts used to synthesize the answer.

## Documentation

* [Guide to adding your own personas](docs/adding%20a%20persona.md)
* [Detailled explanation of the algorithm](docs/inner%20workings.md)

## Potential improvements

* update readme with latest commands

* Set things up to make it easy to install with pip or similar (if possible include dependencies)

* have the persona automatically regenerated if one touches the files in its folder (at best it should be updated rather than recomputed).
* add the possibility of having multiple persona interacting in a single chatb
* add a persona-hub (github repository plus easy way to contribute) and the possibility to download from the hub (could also be decentralised: any github repository with the right file structure)
* Add a non-shell UI

Do not hesitate to submit pull requests to this repository if you find improvements or good alternative prompts!