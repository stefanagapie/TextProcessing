# Text Processing
    This solution will process all the plain text (.txt) files located in the TextProcessing/documents
    folder. Any plain text file may be added are removed from this directory without having to modify 
    the codebase. Once metrics for all the documents have been computed, the output is tabulated, formatted 
    and sent to the terminal. A command line interface (CLI) is provided to allow for customizing of two 
    document filters and one output styling filter. See below for CLI option details.

# Requirements
- `Python 3.10` (A lower minor version might also work)
- `Computer`

# 1. Virtual Environment (Recommended)
#### <mark>From the project's root directory...</mark>
    $ python3.10 -m venv venv

    $ source venv/bin/activate

# 2. Dependencies
#### <mark>From the project's root directory...</mark>
    $ pip install -r requirements.txt

# 3. Command Line Interface (CLI)
#### <mark>From the project's root directory...</mark>
### To run the solution with the default settings
    $ python -m cli
### To run the solution with a word length filter interval between 9 and 11 (inclusive)
    $ python -m cli --word-length-interval 9 11
### To run the solution with a 5 most common word filter
    $ python -m cli --n-common-words 5
### To adjust the sentence column to a width of 150 for the table displaying the document metrics
    $ python -m cli --max-sentence-column-width 150

# Run Tests
#### <mark>From the project's root directory...</mark>
    $ python -m unittest -v

# Assumptions
- Documents are in English.
- Documents are in plain text.
- This solution will not scale without bounds assumption: the average machine has sufficient memory to process a group of documents and therefore the use of a database to store and index document metrics is not needed.
- (I'm sure I've made other assumptions that I don't recall at the moment)

***

* [Project Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
* [Markdown Guide](https://www.markdownguide.org)
