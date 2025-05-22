// Function to append messages to the chat box
function appendMessage(sender, message) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);
    messageDiv.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to handle form submission
document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInput = document.getElementById('userInput').value.trim();
    if (userInput) {
        appendMessage('You', userInput);
        document.getElementById('userInput').value = '';

        // Show typing indicator
        const typingIndicator = document.getElementById('typingIndicator');
        typingIndicator.style.display = 'block';

        // Simulate AI response after a delay
        setTimeout(() => {
            typingIndicator.style.display = 'none';
            const aiResponse = 'This is a simulated AI response.';
            appendMessage('Assistant', aiResponse);
        }, 2000);
    }
});
