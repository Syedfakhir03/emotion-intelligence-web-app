"""Tests for the transformer emotion service."""

import unittest
from unittest.mock import patch

from app.services.emotion_service import emotion_detection


class TestEmotionService(unittest.TestCase):

    def test_empty_text_returns_none(self):
        self.assertIsNone(emotion_detection(""))

    def test_whitespace_returns_none(self):
        self.assertIsNone(emotion_detection("   "))

    def test_non_string_returns_none(self):
        self.assertIsNone(emotion_detection(None))

    @patch("app.services.emotion_service.get_classifier")
    def test_emotion_prediction(self, mock_get_classifier):

        fake_classifier = mock_get_classifier.return_value

        fake_classifier.return_value = [
            {"label": "joy", "score": 0.90},
            {"label": "anger", "score": 0.03},
            {"label": "sadness", "score": 0.02},
            {"label": "fear", "score": 0.02},
            {"label": "neutral", "score": 0.01},
            {"label": "surprise", "score": 0.01},
            {"label": "disgust", "score": 0.01},
        ]

        result = emotion_detection(
            "I am very happy today!"
        )

        self.assertEqual(
            result["dominant_emotion"],
            "joy",
        )

        self.assertAlmostEqual(
            result["emotions"]["joy"],
            0.90,
        )


if __name__ == "__main__":
    unittest.main()