import os
from collections import Counter, defaultdict
from functools import reduce
from operator import add
from pathlib import Path
from typing import Set, List, Dict, Tuple
import nltk


class TokenPattern:
    t0 = r'''(?x)                    # set flag to allow verbose regexps
             (?:[A-Z]\.)+            # abbreviations, e.g. U.S.A.
             | \w+(?:['-]\w+)*       # words with optional internal hyphens or apostrophes (word contractions)
             | \$?\d+(?:[\.,]\d+)?%? # currency and percentages, e.g. $12.40, 82%
             '''

    t1 = r'''(?x)                    # set flag to allow verbose regexps
             (?:[A-Z]\.)+            # abbreviations, e.g. U.S.A.
             | \w+(?:-\w+)*          # words with optional internal hyphens
             | \$?\d+(?:[\.,]\d+)?%? # currency and percentages, e.g. $12.40, 82%
             | \.\.\.                # ellipsis
             | [][.,;"'?():-_`]      # these are separate tokens; includes ], [
             '''


class Document:
    def __init__(self, document_path: Path):
        """
        Model that defines a document from a given text file path.
        :param document_path: A file path
        """
        self._document_path = document_path

    def read(self) -> str:
        """
        Read contents of the entire current document
        :return: document as string
        """
        with open(self._document_path, 'rt') as doc:
            raw = doc.read()
        return raw

    def exists(self) -> bool:
        """
        Check if document exists at the current path
        :return: True if document exists
        """
        return os.path.exists(self._document_path)

    def name(self) -> str:
        """
        The name of the file defined by the document path
        :return: string name of this document
        """
        return Path(self._document_path).name


class DocumentMetrics:
    def __init__(self, doc: 'Document', token_pattern: str = TokenPattern.t0):
        """
        Model that defines the metrics of a given Document
        :param doc: The object that models a text file.
        :param token_pattern: A text pattern that defines words of interest.
        """
        self._doc = doc
        self._token_pattern = token_pattern

        self._sentences: List[str] | None = None
        self._sentence_words: List[List[str]] | None = None
        self._word_sentences_map: Dict[str, List[int]] | None = None
        self._words: List[str] | None = None
        self._words_normalized: List[str] | None = None
        self._word_frequencies: Counter | None = None
        self._vocabulary: Set[str] | None = None
        self._vocabulary_normalized: Set[str] | None = None

    @property
    def document_name(self) -> str:
        return self._doc.name()

    @property
    def sentences(self) -> List[str]:
        """
        Generate a list of sentences from the stored document
        :return: A list of sentences as strings
        """
        if self._sentences is None:
            self._sentences = nltk.sent_tokenize(self._doc.read())
        return self._sentences

    @property
    def sentence_words(self) -> List[List[str]]:
        """
        Generates a list of sentences that are segmented into a list of words
        such that the ith index in the parent list corresponds to a list of
        words

        Example:
            From a sequence of sentences: 'Sentence one.', 'sentence two', ...
            The following is generated: [['Sentence', 'one'], ['sentence', 'two'], ...]

        :return: A list of segmented sentence words as strings
        """
        if self._sentence_words is None:
            sw = [nltk.regexp_tokenize(sentence, self._token_pattern) for sentence in self.sentences]
            self._sentence_words: List[List[str]] = sw
        return self._sentence_words

    @property
    def word_sentences_map(self) -> Dict[str, List[int]]:
        """
        See _build_word_to_sentences_map for documentation.
        """
        if self._word_sentences_map is None:
            self._word_sentences_map = self._build_word_to_sentences_map()
        return self._word_sentences_map

    @property
    def words(self) -> List[str]:
        """
        A list of words that are of interest as defined by
        the token_pattern regex passed to the constructor.
        :return: A list of words that have not been modified.
        """
        if self._words is None:
            self._words = self._flattened_sentence_words(normalize=False)
        return self._words

    @property
    def words_normalized(self) -> List[str]:
        """
        A list of words that are of interest as defined by
        the token_pattern regex passed to the constructor.
        :return: A list of lowercase words.
        """
        if self._words_normalized is None:
            self._words_normalized = self._flattened_sentence_words(normalize=True)
        return self._words_normalized

    @property
    def word_frequencies(self) -> Counter:
        """
        Compute frequency of lowercase words of interest from the given document metrics
        object
        :return: Data structure containing word frequencies
        """
        if self._word_frequencies is None:
            self._word_frequencies = Counter(self.words_normalized)
        return self._word_frequencies

    def vocabulary(self, normalize: bool = True) -> Set[str]:
        """
        Compiles all the words of interest in the current document with the option of
        normalization.
        :param normalize: If True then all compiled words are transformed to lowercase
        :return: The set of words in the current document
        """
        if normalize and self._vocabulary_normalized is None:
            self._vocabulary_normalized = set(self.words_normalized)
        if not normalize and self._vocabulary is None:
            self._vocabulary = set(self.words)
        return self._vocabulary_normalized if normalize else self._vocabulary

    def word_frequency(self, word: str) -> int:
        """
        Frequency of lowercase words of interest.
        :param word: A word of interest in the document
        :return: The number of times the word of interest is observed in this document.
        """
        return self.word_frequencies.get(word.lower(), 0)

    def sentences_containing_word(self, word: str) -> List[str]:
        """
        Find all the sentences that contains at least one occurrence of the given word.
        Note that only words of interest are considered. The words of interest are all
        the words that can be found in the 'self.vocabulary' set.
        :param word: The word to search for in each sentence.
        :return: A list of sentences in string form
        """
        sentence_indices = self.word_sentences_map.get(word.lower(), [])
        return [self.sentences[index] for index in sentence_indices]

    def _build_word_to_sentences_map(self) -> Dict[str, List[int]]:
        """
        Build a data structure that maps normalized words of interest to
        indices of sentences such that the corresponding sentences contain
        at least one occurrence of a key word.
        Example:
            Suppose self.sentences = ['I know you.', 'You are great!', 'Look before you go...']
            Then this data structure would be built as follows:
                {'i': {0},          # because 'I' is located in the first sentence only
                 'know': {0},
                 'you': {0, 1, 2},  # because 'you' is located in the first, second and third sentences
                 'are': {1},
                 ...}

        :return: A dictionary that maps normalized words to sentence indices
        """
        word_sentence_map = defaultdict(set)
        for sentence_index, sentence_words in enumerate(self.sentence_words):
            for sentence_word in sentence_words:
                word_sentence_map[sentence_word.lower()].add(sentence_index)
        return {word: sorted(indices) for word, indices in word_sentence_map.items()}

    def _flattened_sentence_words(self, normalize: bool = True) -> List[str]:
        """
        The _sentence_words data structure is flattened into a single list of
        words where the words are left in there original form or transformed
        to lower case.
        :param normalize: True will transform words to lower case
        :return: A list of words as defined by the token pattern in the __init__ method
        """
        words = reduce(add, self.sentence_words, [])
        return [word.lower() for word in words] if normalize else words


class DocumentsMetrics:
    def __init__(self, docs_metrics: List['DocumentMetrics']):
        """
        Model that defines the aggregate of multiple given DocumentMetrics objects
        :param docs_metrics: The objects that model the metrics of a text file.
        """
        self._docs_metrics = docs_metrics

        self._word_frequencies: Counter | None = None
        self._word_documents_map: Dict[str, List[int]] | None = None

    @property
    def word_frequencies(self) -> Counter:
        """
        Compute frequency of lowercase words of interest from the aggregate document
        metrics objects
        :return: Data structure containing word frequencies
        """
        if self._word_frequencies is None:
            self._word_frequencies = reduce(add, [dm.word_frequencies for dm in self._docs_metrics], Counter())
        return self._word_frequencies

    @property
    def word_document_map(self) -> Dict[str, List[int]]:
        """
        See _build_word_to_document_map for documentation.
        """
        if self._word_documents_map is None:
            self._word_documents_map = self._build_word_to_document_map()
        return self._word_documents_map

    def word_frequency(self, word: str) -> int:
        """
        Frequency of lowercase words of interest.
        :param word: A word of interest in the document
        :return: The number of times the word of interest is observed in this document.
        """
        return self.word_frequencies.get(word.lower(), 0)

    def document_names_containing_word(self, word: str) -> List[str]:
        """
        Find all the documents that contain at least one occurrence of the given word
        from all the provided document metrics objects.
        Note that only words of interest are considered. The words of interest are all
        the words that can be found in the 'self.vocabulary' set in each respective
        document metrics objects.
        :param word: The word to search for in each document.
        :return: A list of document names of string type.
        """
        document_metrics_indices = self.word_document_map.get(word.lower(), [])
        return [self._docs_metrics[index].document_name for index in document_metrics_indices]

    def sentences_containing_word(self, word: str) -> List[str]:
        """
        Find all the sentences that contains at least one occurrence of the given word
        from all the provided document metrics objects.
        Note that only words of interest are considered. The words of interest are all
        the words that can be found in the 'self.vocabulary' set in each respective
        document metrics objects.
        :param word: The word to search for in each sentence.
        :return: A list of sentences in string form
        """
        word = word.lower()
        document_metrics_indices = self.word_document_map.get(word, [])
        documents_metrics = [self._docs_metrics[index] for index in document_metrics_indices]
        sentences = [doc_metrics.sentences_containing_word(word) for doc_metrics in documents_metrics]
        return reduce(add, sentences, [])

    def most_common_words_filtered_by_length(self, length_interval: Tuple[int, int], n: int = None) -> List[Tuple[str, int]]:
        """
        Find n most common words filtered by the length for each word such that the
        length is within the given interval.

        :param length_interval: The interval that the length of a word is checked against
        :param n: At most these number of common words are returned
        :return: A list of word and frequency tuples sorted by frequency in descending order
        """
        frequency_index = 1
        lower, upper = length_interval
        vocabulary = self.word_frequencies.keys()
        common = [(word, self.word_frequency(word)) for word in vocabulary if lower <= len(word) <= upper]
        common.sort(key=lambda tup: tup[frequency_index], reverse=True)
        return common if n is None else common[:n]

    def _build_word_to_document_map(self) -> Dict[str, List[int]]:
        """
        Build a data structure that maps normalized words of interest to document metrics indices
        Example:
            Suppose document one contains self.sentences = ['I know you.', 'You are great!', 'Look before you go...'], and
            suppose document two contains self.sentences = ['We know you.', 'We are not great.', 'Telomeres are critical', ...]
            Then this data structure would be built as follows:
                {'i': {0},          # because 'I' is located in the first document only
                 'know': {0, 1},
                 'you': {0, 1},     # because 'you' is located in the first and in the second document.
                 ...}

        :return: A dictionary that maps normalized words to document indices
        """
        word_document_sentences_map = defaultdict(set)
        for document_index, document in enumerate(self._docs_metrics):
            for word in document.word_sentences_map.keys():
                word_document_sentences_map[word].add(document_index)
        return {word: sorted(indices) for word, indices in word_document_sentences_map.items()}
