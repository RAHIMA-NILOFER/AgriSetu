const toggle = document.getElementById("chatbot-toggle");
const box = document.getElementById("chatbot-box");
const send = document.getElementById("chat-send");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chatbot-messages");

toggle.onclick = () => {
    if (box.style.display === "flex") {
        box.style.display = "none";
    } else {
        box.style.display = "flex";
    }
};

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = type;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {

    const text = input.value.trim();

    if (text === "") return;

    addMessage(text, "user");

    input.value = "";

    const response = await fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: text
        })
    });

    const data = await response.json();

    addMessage(data.reply, "bot");
}

send.onclick = sendMessage;

input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});