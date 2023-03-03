# Adding a persona

To add a persona, add a subfolder in the `personas` folder.

## Folder organization

Your subfolder should:

* be named like your persona (i.e. `John Doe`)
* include texts written by them (if possible in the first person) in a `texts` subfolder

The generation of the persona will generate `index.faiss` and `index.pkl` files containing the extracted information.
Delete those files if you want to regenerate the persona to take new files into account.

Any other file out of the `texts` folder will be ignored, fill free to add notes on the sources of the files, the personality of the persona, etc.

You can place an `about` folder in `texts` to mark texts as being written by someone other than the persona.

See the `persona` folder for various examples.

## File conversion

#### Natively supported formats

`.txt`, `.docx`, `.html` and `.pdf` should be supported natively.

However, images in the files *can* trigger problems with importation (the importer tries to identify elements in the pictures).
I recommend removing them when possible (easy for `.docx` and `.html`, trickier for other formats).

#### Pdf workaround

If you have problems loading `.pdf` files, I would recommend converting them to `.txt`.

To convert a file (say `file.pdf`) to text on a Linux system, you can run the `pdftotext` utility:

```bash
pdftotext file.pdf
```

To convert all `.pdf` files at once, you can run:

```bash
find . -name '*.pdf' -exec pdftotext {} \;
```

If a pdf file is compressed, tripping up the conversion, you can run the following command (warning, this will overwrite your original file):

```bash
qpdf --replace-input --stream-data=uncompress file.pdf file.pdf
```

#### Epub books

`epub` files are not supported at the moment but can be converted to `.html` with [pandoc](https://pandoc.org/).

To convert a file (say `file.epub`) to `.html` on a Linux system, you can run the following command (it will drop images by itself):

```bash
pandoc -f epub -t html -o file.html file.epub
```

To convert all `.epub` files at once, you can run:

```bash
find . -name '*.epub' -exec pandoc -f epub -t html -o {}.html {} \;
```

## What files to use

#### Type of text one could use

To create a persona, you need texts written in the first person by a given author.
Good examples include:

* correspondence
* autobiographies
* blog posts (there are various tools to do so, a simple [wget -r website.com](https://askubuntu.com/a/20469/713860) does the trick)
* some non-fiction and, in particular, self-help books (which are often written in the first person)
* your own chat messages (most chatting platform support downloading your chat history)
* your own diaries or journals
* a short, first-person, description/autobiography of one of your fictional characters
find copyright-free 
Adding a short pseudo-autobiography can be helpful in filling holes in the narrative.

[Project Gutenberg](https://www.gutenberg.org/) and [archive.org](https://archive.org/) are great places to texts (you can even often download them in `.txt` format).

#### Garbage-in, garbage-out

Bad quality or noisy inputs will decrease the quality of your chats.

I recommend cutting the following when possible:

* useless text (table of content, advertisement, html footers, etc)
* irrelevant text
* text written by people other than the person (it might be worth rewriting in the first-person if it is information-rich)
