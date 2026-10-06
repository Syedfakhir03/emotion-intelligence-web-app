const emotionForm =
    document.getElementById("emotionForm");

const textInput =
    document.getElementById("textToAnalyze");

const characterCount =
    document.getElementById("characterCount");

const analyzeButton =
    document.getElementById("analyzeButton");

const buttonText =
    document.getElementById("buttonText");

const buttonLoader =
    document.getElementById("buttonLoader");

const emptyState =
    document.getElementById("emptyState");

const resultsContent =
    document.getElementById("resultsContent");

const dominantEmoji =
    document.getElementById("dominantEmoji");

const dominantEmotion =
    document.getElementById("dominantEmotion");

const dominantScore =
    document.getElementById("dominantScore");

const emotionBars =
    document.getElementById("emotionBars");


const emotionMeta = {

    anger: {
        emoji: "😡",
        color: "#ef4444"
    },

    disgust: {
        emoji: "🤢",
        color: "#22c55e"
    },

    fear: {
        emoji: "😨",
        color: "#8b5cf6"
    },

    joy: {
        emoji: "😄",
        color: "#facc15"
    },

    neutral: {
        emoji: "😐",
        color: "#94a3b8"
    },

    sadness: {
        emoji: "😢",
        color: "#3b82f6"
    },

    surprise: {
        emoji: "😲",
        color: "#f97316"
    }

};


textInput.addEventListener(
    "input",
    updateCharacterCount
);


function updateCharacterCount() {

    const length =
        textInput.value.length;

    characterCount.textContent =
        `${length} character${length === 1 ? "" : "s"}`;
}


document
    .querySelectorAll(".example-chip")
    .forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                textInput.value =
                    button.dataset.text;

                updateCharacterCount();

                textInput.focus();
            }
        );

    });


emotionForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const text =
            textInput.value.trim();

        if (!text) {
            showError(
                "Please enter some text before analyzing."
            );

            return;
        }


        setLoading(true);


        try {

            const response =
                await fetch(
                    "/api/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.error ||
                    "Unable to analyze the text."
                );
            }


            renderResults(data);

        }

        catch (error) {

            console.error(error);

            showError(
                error.message ||
                "Something went wrong."
            );

        }

        finally {

            setLoading(false);

        }

    }
);


function setLoading(isLoading) {

    analyzeButton.disabled =
        isLoading;

    buttonText.textContent =
        isLoading
            ? "Analyzing..."
            : "Analyze Emotion";

    buttonLoader.classList.toggle(
        "hidden",
        !isLoading
    );
}


function renderResults(data) {

    emptyState.classList.add(
        "hidden"
    );

    resultsContent.classList.remove(
        "hidden"
    );


    const dominant =
        data.dominant_emotion.toLowerCase();

    const dominantMeta =
        emotionMeta[dominant] || {
            emoji: "🧠",
            color: "#8b5cf6"
        };


    const score =
        data.emotions[dominant] || 0;


    dominantEmoji.textContent =
        dominantMeta.emoji;

    dominantEmotion.textContent =
        dominant;

    dominantScore.textContent =
        `${(score * 100).toFixed(1)}%`;


    emotionBars.innerHTML = "";


    const sortedEmotions =
        Object.entries(
            data.emotions
        )
        .sort(
            (a, b) =>
                b[1] - a[1]
        );


    sortedEmotions.forEach(
        ([emotion, value]) => {

            const meta =
                emotionMeta[emotion] || {
                    emoji: "•",
                    color: "#8b5cf6"
                };


            const percentage =
                value * 100;


            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "emotion-row";


            row.innerHTML = `
                <div class="emotion-row-header">

                    <div class="emotion-name">

                        <span>
                            ${meta.emoji}
                        </span>

                        <span>
                            ${emotion}
                        </span>

                    </div>

                    <span class="emotion-percentage">
                        ${percentage.toFixed(1)}%
                    </span>

                </div>

                <div class="bar-track">

                    <div
                        class="bar-fill"
                        style="
                            background: ${meta.color};
                        "
                    ></div>

                </div>
            `;


            emotionBars.appendChild(
                row
            );


            const bar =
                row.querySelector(
                    ".bar-fill"
                );


            requestAnimationFrame(
                () => {

                    bar.style.width =
                        `${percentage}%`;

                }
            );

        }
    );

}


function showError(message) {

    emptyState.classList.remove(
        "hidden"
    );

    resultsContent.classList.add(
        "hidden"
    );


    emptyState.innerHTML = `
        <div class="empty-icon">
            !
        </div>

        <h2>
            Unable to analyze
        </h2>

        <p>
            ${message}
        </p>
    `;
}