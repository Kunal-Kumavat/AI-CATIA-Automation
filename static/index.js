const form = document.getElementById('chat-form');
const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const fileInput = document.getElementById('file-input');

const cadImage = document.getElementById('cad-image');
const placeholderText = document.getElementById('placeholder-text');

const imageList = [
  '/static/sample1.png',
  '/static/sample2.png',
  '/static/sample3.png'
]; // Simulated image paths

let currentIndex = 0;

// Initial setup
function showImage(index) {
  if (imageList.length > 0 && imageList[index]) {
    cadImage.src = imageList[index];
    cadImage.classList.remove('hidden');
    placeholderText.classList.add('hidden');
  }
}

// Button Navigation
document.getElementById('prev-btn').addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
    showImage(currentIndex);
  }
});

document.getElementById('next-btn').addEventListener('click', () => {
  if (currentIndex < imageList.length - 1) {
    currentIndex++;
    showImage(currentIndex);
  }
});

// Chat Submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Add user message to chat window
  addMessage('user', message);
  userInput.value = '';

  // Add loading state
  addMessage('bot', 'Processing...');

  // TODO: Integrate backend API call here for real response
  setTimeout(() => {
    updateLastBotMessage(`Running script for: "${message}"`);
    showImage(currentIndex);
  }, 1000);
});

// Chat message DOM update
function addMessage(sender, text) {
  const messageEl = document.createElement('div');
  messageEl.className = `p-2 my-2 rounded-md w-fit max-w-[80%] ${sender === 'user' ? 'bg-blue-100 self-end ml-auto' : 'bg-gray-200'}`;
  messageEl.textContent = text;
  chatWindow.appendChild(messageEl);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateLastBotMessage(text) {
  const messages = chatWindow.querySelectorAll('div');
  const lastBot = [...messages].reverse().find(m => m.classList.contains('bg-gray-200'));
  if (lastBot) lastBot.textContent = text;
}



document.getElementById('file-input').addEventListener('change', function () {
  const form = document.getElementById('upload-form');
  const formData = new FormData(form);

  fetch('/upload', {
    method: 'POST',
    body: formData
  }).then(response => {
    if (response.ok) {
      console.log('File sent to CATIA.');
    } else {
      console.error('Failed to send file.');
    }
  });
});