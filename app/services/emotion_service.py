"""Transformer-based emotion detection service."""

from functools import lru_cache

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)


MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"


def load_tokenizer():
    """Prefer the local cache, then download if necessary."""

    try:
        return AutoTokenizer.from_pretrained(
            MODEL_NAME,
            local_files_only=True,
        )

    except OSError:
        return AutoTokenizer.from_pretrained(
            MODEL_NAME
        )


def load_model():
    """Prefer the local cache, then download if necessary."""

    try:
        return AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            local_files_only=True,
        )

    except OSError:
        return AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME
        )


@lru_cache(maxsize=1)
def get_classifier():
    """Load the classifier once and reuse it."""

    tokenizer = load_tokenizer()
    model = load_model()

    return pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        top_k=None,
    )


def emotion_detection(text_to_analyze):
    """Analyze text and return emotion probabilities."""

    if not isinstance(text_to_analyze, str):
        return None

    text_to_analyze = text_to_analyze.strip()

    if not text_to_analyze:
        return None

    classifier = get_classifier()

    predictions = classifier(text_to_analyze)

    if predictions and isinstance(predictions[0], list):
        predictions = predictions[0]

    emotion_scores = {
        prediction["label"].lower(): float(prediction["score"])
        for prediction in predictions
    }

    dominant_emotion = max(
        emotion_scores,
        key=emotion_scores.get,
    )

    return {
        "emotions": emotion_scores,
        "dominant_emotion": dominant_emotion,
        "model": MODEL_NAME,
    }