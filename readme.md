# Impersonator

*Impersonator* lets you chat with an AI simulation of any author, blogger or person as easily as copy-pasting texts they have written into a folder!

## Installation

You can run the following pip command to install the dependencies (I recommend using a [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments) or [venv](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) environment to isolate the dependencies):

```shell
python3 -m pip install unstructured openai tiktoken bs4 faiss-cpu langchain
```

The `nltk` package (a subdependency) might require some image recognition models to be loaded in order to process pdf inputs.
You can install them with the following command line:

```shell
python3 
```

You can now git clone this repository wherever you want and start to use it!

## Usage

#### Starting Impersonator

To start the program, put your [OpenAI API key](https://platform.openai.com/account/api-keys) in the environment (you can also type it at the beginning of the program) then start `impersonator.py`.

It will display a list of personas available (see [this page](docs/adding%20a%20persona.md) for ways to add personas).
If you select a persona that has never been used, it will first generate it from the data (which will take time proportional to the amount of data in the `texts` subfolder of your persona, probably less than five minutes).

Once your persona is loaded, you can start chatting with it!

#### Commands

You have a handful of special commands available.
To use them, type one of those commands in the chat instead of your message:

* `FREE` lets the persona extrapolate information, filling holes in its knowledge, from now on (the default)
* `STRICT` avoids extrapolation from now on
* `CHECK` will run a fact checker on the persona's latest affirmation,
* `SOURCE` will display the text extracts used to synthesize the answer,
* `REDO` will regenerate the latest answer,
* `EXIT` will terminate the chat.

#### Documentation

* [Guide to adding your own personas](docs/adding%20a%20persona.md)
* [Detailed explanation of the algorithm](docs/inner%20workings.md)

## Potential improvements

* use the chatGPT API to reduce costs and simplify the code
* have the persona be automatically regenerated if one touches the files in its folder (at best it should be updated rather than recomputed)
* add the possibility of having multiple personas interacting in a single chat
* add a persona-hub and the possibility to download from the hub
* Add a non-shell UI

Do not hesitate to submit pull requests to this repository if you find improvements or good alternative prompts!