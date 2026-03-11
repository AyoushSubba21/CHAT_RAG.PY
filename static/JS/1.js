// ================= CHAT FUNCTIONALITY =================

const chatForm = document.getElementById('chat-form');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
let typingIndicator = null;

// Append Message
function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;

    const span = document.createElement('span');
    span.innerHTML = text;

    msgDiv.appendChild(span);
    chatContainer.appendChild(msgDiv);

    if (sender === "user") {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } else {
        msgDiv.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}


// Show Typing Indicator
function showTypingIndicator() {
    if (typingIndicator) return;

    typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message typing';
    typingIndicator.innerHTML = '<span>Assistant is typing...</span>';

    chatContainer.appendChild(typingIndicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove Typing Indicator
function removeTypingIndicator() {
    if (typingIndicator && chatContainer.contains(typingIndicator)) {
        chatContainer.removeChild(typingIndicator);
        typingIndicator = null;
    }
}

// Form Submit
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = userInput.value.trim();
    if (!query) return;

    appendMessage('user', query);

    userInput.value = '';
<<<<<<< Updated upstream
    userInput.disabled = false;
=======
    userInput.disabled = true;
>>>>>>> Stashed changes
    showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query })
        });

        const data = await response.json();

        removeTypingIndicator();

        if (response.ok && data.status === 'success') {
            appendMessage('bot', data.reply);
        } else {
            appendMessage('bot', data.reply || "Something went wrong.");
        }

    } catch (err) {
        removeTypingIndicator();
        appendMessage('bot', "Error: Unable to reach the server.");
        console.error(err);
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
});


// ================= DARK MODE FUNCTIONALITY =================

const toggleBtn = document.getElementById("theme-toggle");

if (toggleBtn) {
    const body = document.body;
    const icon = toggleBtn.querySelector("i");

    // Load Saved Theme OR Detect System Preference
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark" || 
       (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        body.classList.add("dark-mode");
        icon.classList.replace("fa-moon", "fa-sun");
    }

    toggleBtn.addEventListener("click", () => {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            icon.classList.replace("fa-moon", "fa-sun");
            localStorage.setItem("theme", "dark");
        } else {
            icon.classList.replace("fa-sun", "fa-moon");
            localStorage.setItem("theme", "light");
        }
    });
}
// ================= ZOOM FUNCTIONALITY =================

let currentZoom = 100;

const zoomInBtn = document.getElementById("zoom-in");
const zoomOutBtn = document.getElementById("zoom-out");

zoomInBtn.addEventListener("click", () => {
    if (currentZoom < 130) {
        currentZoom += 10;
        document.body.style.zoom = currentZoom + "%";
    }
});

zoomOutBtn.addEventListener("click", () => {
    if (currentZoom > 80) {
        currentZoom -= 10;
        document.body.style.zoom = currentZoom + "%";
    }
});

// ================= INITIAL INPUT CENTER MODE =================

const chatCard = document.querySelector(".chat-card");

// Set initial state on page load
window.addEventListener("DOMContentLoaded", () => {
    chatCard.classList.add("initial-state");
});

// When first message is sent → expand
chatForm.addEventListener("submit", () => {
    if (chatCard.classList.contains("initial-state")) {
        chatCard.classList.remove("initial-state");
        chatCard.classList.add("expanded");
    }
});
