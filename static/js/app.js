const analyzeBtn = document.getElementById("analyze-btn");
const urlInput = document.getElementById("video-url");

const chatSection = document.getElementById("chat-section");
const videoCard = document.getElementById("video-card");
const thumbnail = document.getElementById("video-thumbnail");

const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");


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

    // Clear previous chat
    chatBox.innerHTML = "";
    questionInput.value = "";

    try {

        const result = await loadVideo(url);
        thumbnail.src = result.thumbnail;

        videoCard.classList.remove("hidden");
        chatSection.classList.remove("hidden");
        console.log(result);

        alert("Video Loaded Successfully!");

        chatSection.classList.remove("hidden");

        analyzeBtn.innerHTML = "Analyze Video";

    } catch (error) {

        console.error(error);

        alert("Failed to load video.");

        analyzeBtn.innerHTML = "Analyze Video";

    }

    analyzeBtn.disabled = false;

};


// -----------------------------
// Ask Question
// -----------------------------

sendBtn.onclick = async () => {

    const question = questionInput.value.trim();

    if (question === "") return;

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

        const result = await askQuestion(question);

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