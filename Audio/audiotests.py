import unittest
import utils

class TestContextBridge(unittest.TestCase):

	def setUp(self):
		self.words_22 = "a b c d e f g h i j k l m n o p q r s t u v"
		self.words_5  = "a b c d e"
		self.words_20 = "a b c d e f g h i j k l m n o p q r s t"
		self.words_empty = ""

	def test_more_than_20(self):
		self.assertEqual(utils.getLast20Words(self.words_22), "c d e f g h i j k l m n o p q r s t u v")

	def test_less_than_20(self):
		self.assertEqual(utils.getLast20Words(self.words_5), self.words_5)

	def test_20_20(self):
		self.assertEqual(utils.getLast20Words(self.words_20), self.words_20)

	def test_empty(self):
		self.assertEqual(utils.getLast20Words(self.words_empty), self.words_empty)

class TestCloudFileStorage(unittest.TestCase):

	def test_local_file_not_found(self):
		with self.assertRaises(FileNotFoundError):
			utils.upload_to_aws("bogus_123", "", "")

if __name__ == '__main__':
    unittest.main()