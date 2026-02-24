const chatForm = document.getElementById('chat-form');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
let typingIndicator = null;

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;

    const span = document.createElement('span');
    span.innerText = text;

    msgDiv.appendChild(span);
    chatContainer.appendChild(msgDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}


appendMessage('bot', "Namaste. I am your Digital Mitra. How may I assist you today?");

function showTypingIndicator() {
    typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message typing';
    typingIndicator.innerHTML = '<span>Assistant is typing...</span>';

    chatContainer.appendChild(typingIndicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    if (typingIndicator) {
        chatContainer.removeChild(typingIndicator);
        typingIndicator = null;
    }
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = userInput.value.trim();
    if (!query) return;

    appendMessage('user', query);

    userInput.value = '';
    userInput.disabled = true;
    showTypingIndicator();
    try {
      
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: query
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            appendMessage('bot', data.reply);
        } else {
            appendMessage('bot', "Something went wrong.");
        }
        removeTypingIndicator();

    } catch (err) {
        appendMessage('bot', "Error: Unable to reach the server.");
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
});