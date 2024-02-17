import unittest
import utils
import os
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment

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

class TestAudioCreation(unittest.TestCase):

	def setUp(self):
		self.client = client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
		self.textInput = "This is a test of some text for tts conversion."

	def test_audio_file_creation(self):
		fileName = Path(__file__).parent / f"test_output.wav"
		response = self.client.audio.speech.create(model="tts-1-hd", voice="onyx", input=self.textInput)
		response.write_to_file(fileName)

		self.assertTrue(os.path.getsize(fileName) > 1)
		os.remove(fileName)

	def test_audio_file_duration(self):
		fileName = Path(__file__).parent / f"test_output.wav"
		response = self.client.audio.speech.create(model="tts-1-hd", voice="onyx", input=self.textInput)
		response.write_to_file(fileName)
		self.assertTrue(AudioSegment.from_file(fileName).duration_seconds > 1)
		os.remove(fileName)

		
	def test_stitch_audio_files_together(self):
		baseFileName = "test_audio_output"
		finalOutputName = "test_combined_audio.mp3"
		finalOutputPath = Path(__file__).parent / finalOutputName
		test_string = "this is a test"
		merged = AudioSegment.empty()

		i = 0
		for word in test_string.split():
			self.client.audio.speech.create(model="tts-1-hd", voice="onyx", input=word).write_to_file(
				Path(__file__).parent / (baseFileName + str(i))
				)
			merged += AudioSegment.from_file(Path(__file__).parent / (baseFileName + str(i)))
			i += 1
		merged.export(finalOutputName, format="mp3", bitrate="192k")

		self.assertTrue(AudioSegment.from_file(finalOutputPath).duration_seconds > 1)
		self.assertTrue(AudioSegment.from_file(finalOutputPath).duration_seconds > 
			AudioSegment.from_file(Path(__file__).parent / (baseFileName + '0')).duration_seconds)

		os.remove(finalOutputPath)

		i = 0
		for word in test_string.split():
			os.remove(Path(__file__).parent / (baseFileName + str(i)))
			i += 1


if __name__ == '__main__':
    unittest.main()