"""Tests for the Emotion Intelligence API."""

import unittest
from unittest.mock import patch

from app import create_app


class TestEmotionRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        self.app.config["TESTING"] = True

        self.client = self.app.test_client()

    def test_home_page(self):

        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_analyze_requires_text(self):

        response = self.client.post(
            "/api/analyze",
            json={"text": ""},
        )

        data = response.get_json()

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            data["success"]
        )

    @patch("app.routes.emotion_detection")
    def test_analyze_success(
        self,
        mock_emotion_detection,
    ):

        mock_emotion_detection.return_value = {
            "emotions": {
                "joy": 0.91,
                "anger": 0.02,
                "sadness": 0.02,
                "fear": 0.01,
                "neutral": 0.01,
                "surprise": 0.02,
                "disgust": 0.01,
            },
            "dominant_emotion": "joy",
            "model":
                "j-hartmann/"
                "emotion-english-distilroberta-base",
        }

        response = self.client.post(
            "/api/analyze",
            json={
                "text":
                    "I am very happy today!"
            },
        )

        data = response.get_json()

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["dominant_emotion"],
            "joy",
        )


if __name__ == "__main__":
    unittest.main()