async function runEmotionAnalysis() {
    const textInput = document.getElementById("textToAnalyze");
    const responseContainer = document.getElementById("system_response");

    const text = textInput.value.trim();

    if (!text) {
        responseContainer.innerHTML =
            "Please enter some text before analyzing.";
        return;
    }

    responseContainer.innerHTML = "Analyzing...";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            responseContainer.innerHTML =
                data.error || "Unable to analyze the text.";
            return;
        }

        const emotions = data.emotions;

        let emotionOutput = "";

        for (const [emotion, score] of Object.entries(emotions)) {
            const percentage = (score * 100).toFixed(1);

            emotionOutput += `
                <div>
                    <strong>${emotion}</strong>:
                    ${percentage}%
                </div>
            `;
        }

        responseContainer.innerHTML = `
            <h4>Dominant Emotion:
                ${data.dominant_emotion.toUpperCase()}
            </h4>

            <hr>

            ${emotionOutput}
        `;

    } catch (error) {
        console.error(error);

        responseContainer.innerHTML =
            "Something went wrong while analyzing the text.";
    }
}