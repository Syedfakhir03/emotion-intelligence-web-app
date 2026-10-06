"""Flask routes for the Emotion Intelligence application."""

from flask import jsonify, render_template, request

from app.services.emotion_service import emotion_detection


def register_routes(app):
    """Register application routes."""

    @app.route("/")
    def index():
        """Display the main application page."""
        return render_template("index.html")


    @app.route("/api/analyze", methods=["POST"])
    def analyze_emotion():
        """Analyze text and return structured JSON."""

        data = request.get_json(silent=True) or {}

        text = data.get("text", "")

        if not isinstance(text, str) or not text.strip():
            return jsonify(
                {
                    "success": False,
                    "error": "Please provide some text to analyze.",
                }
            ), 400

        result = emotion_detection(text)

        if result is None:
            return jsonify(
                {
                    "success": False,
                    "error": "Unable to analyze the provided text.",
                }
            ), 500

        return jsonify(
            {
                "success": True,
                "text": text.strip(),
                "emotions": result["emotions"],
                "dominant_emotion": result["dominant_emotion"],
            }
        )