import unittest
from pathlib import Path
from src.document_metrics import Document
from src.document_metrics import DocumentMetrics


class TestDocumentMetrics(unittest.TestCase):
    test_assets_path: Path = Path(__file__).parent / 'assets'

    empty_document_name: str = 'doc_empty.txt'
    mixed_characters_document_name: str = 'doc_mixed_characters.txt'
    single_sentence_document_name: str = 'doc_single_sentence.txt'
    two_simple_sentence_document_name: str = 'doc_two_simple_sentences.txt'
    multiple_sentences_document_name: str = 'doc_five_sentences.txt'
    multiple_lines_document_name: str = 'doc_multiple_lines.txt'

    @staticmethod
    def doc_path(doc_name: str):
        return TestDocumentMetrics.test_assets_path / doc_name


class TestSentenceExtraction(TestDocumentMetrics):

    def test_sentence_extraction_of_zero_result(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentences
        expected = []
        self.assertEqual(expected, actual)

    def test_sentence_extraction_of_one_result(self):
        document = Document(self.doc_path(self.single_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = len(doc_stats.sentences)
        expected = 1
        self.assertEqual(expected, actual)

    def test_sentence_extraction_of_multiple_results(self):
        document = Document(self.doc_path(self.multiple_sentences_document_name))
        doc_stats = DocumentMetrics(document)
        actual = len(doc_stats.sentences)
        expected = 5
        self.assertEqual(expected, actual)


class TestWordExtraction(TestDocumentMetrics):

    def test_word_extraction_from_mixed_characters_doc_with_t0_token_pattern(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.vocabulary(False)
        expected = {'Let', 'me', 'begin', 'by', 'saying', 'thanks', 'to', 'all', 'you', "who've",
                    'traveled', "It's", 'humbling', 'but', 'in', 'my', 'heart', 'I', 'know', 'you',
                    "didn't", 'come', 'high-spirited', 'and', 'know-it-all', 'people', 'are', 'shallow',
                    'enclosed', '13400400', '$123', '$13.40', '$13,400'}
        self.assertEqual(expected, actual)

    def test_normalized_word_extraction_from_mixed_characters_doc_with_t0_token_pattern(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.vocabulary(True)
        expected = {'let', 'me', 'begin', 'by', 'saying', 'thanks', 'to', 'all', 'you', "who've",
                    'traveled', "it's", 'humbling', 'but', 'in', 'my', 'heart', 'i', 'know', 'you',
                    "didn't", 'come', 'high-spirited', 'and', 'know-it-all', 'people', 'are', 'shallow',
                    'enclosed', '13400400', '$123', '$13.40', '$13,400'}
        self.assertEqual(expected, actual)

    def test_zero_sentence_segmentation(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentence_words
        expected = []
        self.assertEqual(expected, actual)

    def test_single_sentence_segmentation(self):
        document = Document(self.doc_path(self.single_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentence_words
        expected = [["I'm", 'a', 'lonely', 'sentence']]
        self.assertEqual(expected, actual)

    def test_two_sentence_segmentation(self):
        document = Document(self.doc_path(self.two_simple_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentence_words
        expected = [["I'm", 'the', 'first', 'sentence', 'of', 'two'],
                    ["I'm", 'the', 'next', 'sentence', 'in', 'the', 'list', 'of', 'two', 'sentences', 'in', 'total']]
        self.assertEqual(expected, actual)

    def test_word_extraction_of_empty_document(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words
        expected = []
        self.assertEqual(expected, actual)

    def test_word_extraction_of_single_sentence_document(self):
        document = Document(self.doc_path(self.single_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words
        expected = ["I'm", 'a', 'lonely', 'sentence']
        self.assertEqual(expected, actual)

    def test_word_extraction_of_two_sentence_document(self):
        document = Document(self.doc_path(self.two_simple_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words
        expected = ["I'm", 'the', 'first', 'sentence', 'of', 'two', "I'm", 'the', 'next', 'sentence', 'in', 'the', 'list', 'of', 'two', 'sentences', 'in', 'total']
        self.assertEqual(expected, actual)

    def test_normalized_word_extraction_of_empty_document(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words_normalized
        expected = []
        self.assertEqual(expected, actual)

    def test_normalized_word_extraction_of_single_sentence_document(self):
        document = Document(self.doc_path(self.single_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words_normalized
        expected = ["i'm", 'a', 'lonely', 'sentence']
        self.assertEqual(expected, actual)

    def test_normalized_word_extraction_of_two_sentence_document(self):
        document = Document(self.doc_path(self.two_simple_sentence_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.words_normalized
        expected = ["i'm", 'the', 'first', 'sentence', 'of', 'two', "i'm", 'the', 'next', 'sentence', 'in', 'the', 'list', 'of', 'two', 'sentences', 'in', 'total']
        self.assertEqual(expected, actual)


class TestWordToSentencesCorrespondence(TestDocumentMetrics):

    def test_word_corresponds_to_zero_sentence_of_empty_document(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentences_containing_word('any')
        expected = []
        self.assertEqual(expected, actual)

    def test_word_corresponds_to_zero_sentence_of_multi_line_document(self):
        document = Document(self.doc_path(self.multiple_lines_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentences_containing_word('any')
        expected = []
        self.assertEqual(expected, actual)

    def test_word_corresponds_to_one_sentence_of_multi_line_document(self):
        document = Document(self.doc_path(self.multiple_lines_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentences_containing_word('humbling')
        expected = ["It's humbling, but in my heart I know you didn't come here just for me, you came here because you believe in what this country can be."]
        self.assertEqual(expected, actual)

    def test_word_corresponds_to_two_sentences_of_multi_line_document(self):
        document = Document(self.doc_path(self.multiple_lines_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.sentences_containing_word('me')
        expected = ["Let me begin by saying thanks to all you who've traveled, from far and wide, to brave the cold today.",
                    "It's humbling, but in my heart I know you didn't come here just for me, you came here because you believe in what this country can be."]
        self.assertEqual(expected, actual)


class TestDocumentName(TestDocumentMetrics):

    def test_correct_retrieval_of_filename_from_document(self):
        document = Document(self.doc_path(self.empty_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.document_name
        expected = self.empty_document_name
        self.assertEqual(expected, actual)


class TestWordFrequency(TestDocumentMetrics):

    def test_word_frequency_of_zero_result(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.word_frequency('SpaceX')
        expected = 0
        self.assertEqual(expected, actual)

    def test_capitalized_word_frequency_of_one_result(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.word_frequency('Shallow')
        expected = 1
        self.assertEqual(expected, actual)

    def test_lowercase_word_frequency_of_one_result(self):
        # TODO: combine with above test as subtests
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.word_frequency('shallow')
        expected = 1
        self.assertEqual(expected, actual)

    def test_price_word_frequency_of_one_result(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.word_frequency('$13,400')
        expected = 1
        self.assertEqual(expected, actual)

    def test_word_frequency_of_two_results(self):
        document = Document(self.doc_path(self.mixed_characters_document_name))
        doc_stats = DocumentMetrics(document)
        actual = doc_stats.word_frequency('you')
        expected = 2
        self.assertEqual(expected, actual)
