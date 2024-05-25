// File Path: appsai/static/js/scripts.js

// File Path: appsai/static/js/scripts.js

// Function to scroll to the bottom of the chat box
function scrollToBottom() {
    var chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Scroll to the bottom on page load
window.onload = function() {
    scrollToBottom();
};

// Scroll to the bottom on form submission
document.getElementById('chat-form').onsubmit = function() {
    setTimeout(scrollToBottom, 100);
};

// Auto-resize the textarea
const textarea = document.querySelector('textarea');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});

// Submit the form when Enter key is pressed
textarea.addEventListener('keypress', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        document.getElementById('chat-form').submit();
    }
});

// MutationObserver to watch for new messages and scroll to the bottom
var chatBox = document.getElementById('chat-box');
var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        scrollToBottom();
    });
});

// Observe changes to the chat box
observer.observe(chatBox, { childList: true });
