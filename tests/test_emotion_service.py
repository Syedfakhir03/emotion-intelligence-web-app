"""Tests for the emotion detection service."""

import unittest

from app.services.emotion_service import emotion_detection


class TestEmotionDetection(unittest.TestCase):
    """Test emotion classification examples."""

    def test_joy(self):
        result = emotion_detection(
            "I am glad this happened"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "joy",
        )


    def test_anger(self):
        result = emotion_detection(
            "I am really mad about this"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "anger",
        )


    def test_disgust(self):
        result = emotion_detection(
            "I feel disgusted just hearing about this"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "disgust",
        )


    def test_sadness(self):
        result = emotion_detection(
            "I am so sad about this"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "sadness",
        )


    def test_fear(self):
        result = emotion_detection(
            "I am really afraid that this will happen"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "fear",
        )


if __name__ == "__main__":
    unittest.main()