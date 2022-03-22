from textwrap import wrap
from pathlib import Path
from typing import List

from tabulate import tabulate

from document_metrics import Document, DocumentMetrics, DocumentsMetrics


class EigenCLIView:
    """
    Defines how the coding task displays to the command line document metrics.
    """

    def __init__(
            self,
            word_length_interval: tuple[int, int],
            n_common_words: int,
            tabulated_data: list[tuple],
            tabulated_data_headers: list[str]
    ):
        self._word_length_interval = word_length_interval
        self._n_common_words = n_common_words
        self._tabulated_data = tabulated_data
        self._tabulated_data_headers = tabulated_data_headers

    def display(self):

        table = tabulate(
            self._tabulated_data,
            headers=self._tabulated_data_headers,
            showindex=True,
            tablefmt='fancy_grid',
        )
        print()
        print(f'[*] Showing most common words with the following predicates:')
        print(f'       i. Word lengths are within the interval of {self._word_length_interval}, and')
        print(f'      ii. {self._n_common_words} most common elements from the most common to the least.')
        print(table)


class EigenController:
    """
    Defines how the document metrics are gathered and assigns a view object for deciding how to display the data.
    """

    @staticmethod
    def _textwrap(sentence: str, width: int) -> str:
        return '\n'.join(wrap(sentence, width=width, replace_whitespace=False, fix_sentence_endings=True))

    @staticmethod
    def text_file_paths() -> List[Path]:
        """
        Gather all the text files from the project's documents folder (non-recursive)
        :return: A list of text file paths
        """
        documents_path = Path(__file__).parent.parent / 'documents'
        file_paths = documents_path.iterdir()
        return [file for file in file_paths if file.is_file() and file.suffix == '.txt']

    @staticmethod
    def metrics(file_paths: List[Path]) -> DocumentsMetrics:
        documents = [Document(file_path) for file_path in file_paths]
        documents_metrics = [DocumentMetrics(document) for document in documents]
        return DocumentsMetrics(documents_metrics)

    def run(self, word_length_interval: tuple[int, int], n_common_words: int, max_sentence_width):
        file_paths = self.text_file_paths()
        metrics = self.metrics(file_paths)
        words_of_interest = metrics.most_common_words_filtered_by_length(word_length_interval, n_common_words)

        table = []
        table_headers = ['Word (Total Occurrences)', 'Documents', 'Sentences containing the word']
        for word, frequency in words_of_interest:
            word_occurrence = f'{word.capitalize()} ({frequency})'
            document_names = '\n'.join(sorted(metrics.document_names_containing_word(word)))
            sentences = '\n\n'.join(self._textwrap(sente, max_sentence_width) for sente in metrics.sentences_containing_word(word))
            table.append((word_occurrence, document_names, sentences))

        EigenCLIView(word_length_interval, n_common_words, table, table_headers).display()
