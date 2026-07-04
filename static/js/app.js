const analyzeBtn = document.getElementById("analyze-btn");
const urlInput = document.getElementById("video-url");

const chatSection = document.getElementById("chat-section");
const videoCard = document.getElementById("video-card");
const thumbnail = document.getElementById("video-thumbnail");

const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");

let sessionId = null;


// -----------------------------
// Analyze Video
// -----------------------------

analyzeBtn.onclick = async () => {

    const url = urlInput.value.trim();

    if (url === "") {
        alert("Please enter a YouTube URL.");
        return;
    }

    analyzeBtn.innerHTML = "Loading...";
    analyzeBtn.disabled = true;

    chatBox.innerHTML = "";
    questionInput.value = "";

    try {

        const result = await loadVideo(url);

        if (result.status === "error") {
            alert(result.message);
            analyzeBtn.innerHTML = "Analyze Video";
            analyzeBtn.disabled = false;
            return;
        }

        sessionId = result.session_id;

        thumbnail.src = result.thumbnail;

        videoCard.classList.remove("hidden");
        chatSection.classList.remove("hidden");

        alert("Video Loaded Successfully!");

    } catch (error) {

        console.error(error);

        alert("Failed to load video.");

    }

    analyzeBtn.innerHTML = "Analyze Video";
    analyzeBtn.disabled = false;

};


// -----------------------------
// Ask Question
// -----------------------------

sendBtn.onclick = async () => {

    const question = questionInput.value.trim();

    if (question === "") return;

    if (!sessionId) {
        alert("Please load a video first.");
        return;
    }

    chatBox.innerHTML += `
        <div class="user-msg">
            ${question}
        </div>
    `;

    questionInput.value = "";

    chatBox.innerHTML += `
        <div id="loading" class="ai-msg">
            Thinking...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const result = await askQuestion(question, sessionId);

        document.getElementById("loading").remove();

        chatBox.innerHTML += `
            <div class="ai-msg">
                ${result.answer}
            </div>
        `;

    } catch (error) {

        document.getElementById("loading").remove();

        chatBox.innerHTML += `
            <div class="ai-msg">
                Something went wrong.
            </div>
        `;

    }

    chatBox.scrollTop = chatBox.scrollHeight;

};


// -----------------------------
// Press Enter to Send
// -----------------------------

questionInput.addEventListener("keypress", (event) => {

    if (event.key === "Enter") {

        sendBtn.click();

    }

});