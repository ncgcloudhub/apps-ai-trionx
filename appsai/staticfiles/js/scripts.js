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

// Function to get the file type class
function getFileTypeClass(fileName) {
    const ext = fileName.split('.').pop().toLowerCase();
    switch (ext) {
        case 'pdf':
            return 'pdf';
        case 'jpeg':
        case 'jpg':
        case 'png':
        case 'webp':
            return 'image';
        case 'txt':
            return 'text';
        case 'doc':
        case 'docx':
            return 'docs';
        case 'csv':
            return 'csv';
        default:
            return 'default';
    }
}

// Display file names when files are selected
document.getElementById('file-input').addEventListener('change', function() { // Ensure this function updates the file attachments display
    const fileInput = this;
    const fileAttachments = document.getElementById('file-attachments');
    fileAttachments.innerHTML = ''; // Clear previous attachments
    for (const file of fileInput.files) {
        const fileElement = document.createElement('div');
        fileElement.classList.add('file-attachment');
        //fileElement.innerHTML = `<i class="bi bi-file-earmark ${getFileTypeClass}"></i> ${file.name}`;
        const fileTypeClass = getFileTypeClass(file.name); // Correctly call the function here
        fileElement.innerHTML = `<i class="bi bi-file-earmark ${fileTypeClass} file-icon"></i> ${file.name}`; // Ensure 'file-icon' class is included
        fileAttachments.appendChild(fileElement);
    }
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



document.addEventListener('DOMContentLoaded', function() {
    // Ensure dropdowns are working
    var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
    var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl)
    })
})

