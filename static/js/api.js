async function loadVideo(url) {

    const response = await fetch("/load-video", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            url: url
        })

    });

    return response.json();

}


async function askQuestion(question, sessionId) {

    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question,
            session_id: sessionId
        })

    });

    return response.json();

}