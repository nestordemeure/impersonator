# Inner-Workings

This repository is an application of [Large Language Models](https://en.wikipedia.org/wiki/Wikipedia:Large_language_models) and, in particular, [GPT-3](https://en.wikipedia.org/wiki/GPT-3).

It relies on [LangChain](https://github.com/hwchase17/langchain) to interface the various language models and functionalities together.

## 0. Data storage

When a persona is created, its texts are:
* split into chunks, 
* turned into embeddings using [OpenAI's text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/second-generation-models)
* stored in a [FAISS vector database](https://faiss.ai/) that is written to disk

## 1. Similarity search

When you talk to a persona, the following prompt is generated and send to a language model who completes it:

```
The following chat ends on a question by {user_name}.
Write a list of queries to google the answer to {user_name}'s last question.
Use precise words, don't be afraid of using synonyms.

CHAT:
{chat_history}

GOOGLE: {name}
```

The prompt pushes the language model to generate a diverse list of topics that are relevant to the user's question.
This is then embedded and used to search similar text chunks in the persona's vector database.

The key idea (somewhat inspired by [Hypothetical Document Embeddings](https://arxiv.org/abs/2212.10496)) is that raw questions my not embed that close to their answer.

## 2. Question answering

Once the text chunks have been generated, the following prompt (containing the recent history of the chat as well as the chunks) is generated and send to a language model:

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

Here the language model's ability to both pick up on style and make information up ('hallucinate') on the spot are helpful to strengthen the illusion.

## Bonus. Fact checking

Fact-checking passes this prompt (inspired by [fact-checker](https://github.com/jagilley/fact-checker)) to the language model:

```
The following texts have been written by {name}.

SOURCES:
{extracts}

ASSERTION:
{name}: {answer}

The sources are all true.
Determine whether the assertion is true or false. If it is false, explain why.
```

It checks the persona's latest affirmation against the text chunks it was passed.

The repository also contains a unused alternative question-answering prompt (under the name `PROMPT_ANSWER_REDUCED_HALUCINATIONS`) that, combined with a lower model temperature, is mostly successful at eliminating hallucinations (it however hurts the flow of the conversation):

```
You are {name} and are having a sourced conversation.
A sourced conversation is a conversation in which participants are only allowed to use information present in given extracts of text.
You are given the following extracts of texts you have written and the latest messages in the conversation.
Provide a conversational answer. Stay close to the style and voice of your texts.
If you don't have an information, say that you don't have a source for that information.

EXTRACTS:
{extracts}

CHAT:
{chat_history}
{name}:
```