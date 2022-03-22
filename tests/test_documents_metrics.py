import unittest
from pathlib import Path
from collections import defaultdict
from src.document_metrics import Document
from src.document_metrics import DocumentMetrics
from src.document_metrics import DocumentsMetrics


class TestDocumentMetrics(unittest.TestCase):
    test_assets_path: Path = Path(__file__).parent / 'assets'

    empty_document_name: str = 'doc_empty.txt'
    document_one_name: str = 'doc1.txt'
    document_two_name: str = 'doc2.txt'
    document_three_name: str = 'doc3.txt'
    multiple_lines_document_name: str = 'doc_multiple_lines.txt'

    @staticmethod
    def doc_path(doc_name: str):
        return TestDocumentMetrics.test_assets_path / doc_name


class TestWordFrequency(TestDocumentMetrics):

    def setUp(self) -> None:
        doc_names = [self.document_one_name, self.document_two_name]
        docs = [Document(self.doc_path(name)) for name in doc_names]
        docs_metrics = [DocumentMetrics(doc) for doc in docs]
        self.doc_aggregate_metrics = DocumentsMetrics(docs_metrics)

    def test_aggregate_frequency_of_word_not_appearing_in_any_document(self):

        expected = 0
        for search_word in ['Telomeres', 'telomeres']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.word_frequency(search_word)
                self.assertEqual(expected, actual)

    def test_aggregate_frequency_of_word_appearing_in_multiple_documents(self):

        expected = 228
        for search_word in ['To', 'to']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.word_frequency(search_word)
                self.assertEqual(expected, actual)

    def test_aggregate_frequency_of_word_appearing_in_one_document(self):

        expected = 1
        for search_word in ['Try', 'try']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.word_frequency(search_word)
                self.assertEqual(expected, actual)


class TestWordToSentencesCorrespondence(TestDocumentMetrics):

    def setUp(self) -> None:
        doc_names = [self.document_one_name, self.document_two_name]
        docs = [Document(self.doc_path(name)) for name in doc_names]
        docs_metrics = [DocumentMetrics(doc) for doc in docs]
        self.doc_aggregate_metrics = DocumentsMetrics(docs_metrics)

    def test_word_correspondence_to_single_sentence_of_one_of_two_documents(self):
        expected = [
            'You understand that in this election, the greatest risk we can take is to try the same old politics with the same old players and expect a different result.'
        ]
        for search_word in ['Try', 'try']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.sentences_containing_word(search_word)
                self.assertEqual(expected, actual)

    def test_word_correspondence_to_zero_sentences_of_two_documents(self):
        expected = []
        for search_word in ['Trying', 'trying']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.sentences_containing_word(search_word)
                self.assertEqual(expected, actual)

    def test_word_correspondence_to_six_sentences_of_two_documents(self):
        expected = [
            "All of us know what those challenges are today - a war with no end, a dependence on oil that threatens our future, schools where too many children aren't learning, and families struggling paycheck to paycheck despite working as hard as they can.",
            "Let's be the generation that finally frees America from the tyranny of oil.",
            "How else could he propose hundreds of billions in tax breaks for big corporations and oil companies but not one penny of tax relief to more than one hundred million Americans?",
            "And for the sake of our economy, our security, and the future of our planet, I will set a clear goal as President: in ten years, we will finally end our dependence on oil from the Middle East.",
            "Washington's been talking about our oil addiction for the last thirty years, and John McCain has been there for twenty-six of them.",
            "And today, we import triple the amount of oil as the day that Senator McCain took office.",
        ]
        for search_word in ['Oil', 'oil']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.sentences_containing_word(search_word)
                self.assertEqual(expected, actual)


class TestWordToDocumentNamesCorrespondence(TestDocumentMetrics):

    def setUp(self) -> None:
        doc_names = [self.document_one_name, self.document_two_name, self.document_three_name]
        docs = [Document(self.doc_path(name)) for name in doc_names]
        docs_metrics = [DocumentMetrics(doc) for doc in docs]
        self.doc_aggregate_metrics = DocumentsMetrics(docs_metrics)

    def test_word_correspondence_to_no_document_of_three_documents(self):
        expected = []
        for search_word in ['Trunk', 'trunk']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.document_names_containing_word(search_word)
                self.assertEqual(expected, actual)

    def test_word_correspondence_to_third_document_of_three_documents(self):
        expected = ['doc3.txt']
        for search_word in ['Trying', 'trying']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.document_names_containing_word(search_word)
                self.assertEqual(expected, actual)

    def test_word_correspondence_to_all_documents_of_three_documents(self):
        expected = ['doc1.txt', 'doc2.txt', 'doc3.txt']
        for search_word in ['Oil', 'oil']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.document_names_containing_word(search_word)
                self.assertEqual(expected, actual)

    def test_word_correspondence_to_second_document_of_three_documents(self):
        expected = ['doc2.txt']
        for search_word in ['Direct', 'direct']:
            with self.subTest(word=search_word):
                actual = self.doc_aggregate_metrics.document_names_containing_word(search_word)
                self.assertEqual(expected, actual)


class MostCommonWordShared:
    @staticmethod
    def anonymize_words_and_map(common_words):
        # this mapping is needed since the method under test
        # is non-deterministic in the actual word that is returned
        word_freq = defaultdict(list)
        for word, frequency in common_words:
            anon = 'X' * len(word)
            word_freq[anon].append(frequency)
        return word_freq


class TestMostCommonWordOnSingleDocument(TestDocumentMetrics, MostCommonWordShared):

    def setUp(self) -> None:
        document = Document(self.doc_path(self.multiple_lines_document_name))
        doc_stats = DocumentMetrics(document)
        self.docs_stats = DocumentsMetrics([doc_stats])

    def test_two_most_common_of_length_interval_1_to_1(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((1, 1), 2)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('a', 1), ('i', 1)])
        self.assertEqual(expected, actual)

    def test_two_most_common_of_length_interval_3_to_5(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((3, 5), 2)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('you', 6), ('can', 3)])
        self.assertEqual(expected, actual)

    def test_three_most_common_of_length_interval_3_to_5(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((3, 5), 3)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('you', 6), ('can', 3), ('the', 3)])
        self.assertEqual(expected, actual)

    def test_most_common_of_length_interval_5_to_6(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((5, 6))
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('there', 2), ('begin', 1), ('saying', 1), ('heart', 1), ('today', 1), ("didn't", 1), ('reason', 1), ("who've", 1), ('thanks', 1), ('brave', 1), ('peace', 1)])
        self.assertEqual(expected, actual)


class TestMostCommonWordOnMultipleDocuments(TestDocumentMetrics, MostCommonWordShared):

    def setUp(self) -> None:
        document1 = Document(self.doc_path(self.multiple_lines_document_name))
        document2 = Document(self.doc_path(self.multiple_lines_document_name))
        doc_stats1 = DocumentMetrics(document1)
        doc_stats2 = DocumentMetrics(document2)
        self.docs_stats = DocumentsMetrics([doc_stats1, doc_stats2])

    def test_two_most_common_of_length_interval_1_to_1(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((1, 1), 2)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('a', 2), ('i', 2)])
        self.assertEqual(expected, actual)

    def test_two_most_common_of_length_interval_3_to_5(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((3, 5), 2)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('you', 12), ('can', 6)])
        self.assertEqual(expected, actual)

    def test_three_most_common_of_length_interval_3_to_5(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((3, 5), 3)
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('you', 12), ('can', 6), ('the', 6)])
        self.assertEqual(expected, actual)

    def test_most_common_of_length_interval_5_to_6(self):
        actual = self.docs_stats.most_common_words_filtered_by_length((5, 6))
        actual = self.anonymize_words_and_map(actual)
        expected = self.anonymize_words_and_map([('there', 4), ('begin', 2), ('saying', 2), ('heart', 2), ('today', 2), ("didn't", 2), ('reason', 2), ("who've", 2), ('thanks', 2), ('brave', 2), ('peace', 2)])
        self.assertEqual(expected, actual)
