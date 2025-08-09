function returnHome() {
  window.location.href = "/home"
}



const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

const userAvatar = "https://storage.googleapis.com/a1aa/image/759f54fa-e944-4d63-2afc-58cf0ca0a33b.jpg";
const botAvatar = "https://storage.googleapis.com/a1aa/image/274f13c7-ae6c-431b-7bfd-63c436fc4bef.jpg";

// Function to create user message div aligned right
function createUserMessage(message) {
  const wrapper = document.createElement('div');
  wrapper.className = 'flex justify-end max-w-xl';

  const messageBox = document.createElement('div');
  messageBox.className = 'bg-[#19707a] text-white rounded-xl px-6 py-4 text-sm leading-relaxed max-w-[400px] break-words';
  messageBox.textContent = message;

  const avatar = document.createElement('img');
  avatar.src = userAvatar;
  avatar.alt = 'User avatar';
  avatar.className = 'rounded-full ml-3 w-8 h-8 object-cover border border-gray-200 shadow-sm flex-shrink-0'; 

  wrapper.appendChild(messageBox);
  wrapper.appendChild(avatar);

  return wrapper;
}

// Function to create bot message div aligned left
function createBotMessage(message) {
  const wrapper = document.createElement('div');
  wrapper.className = 'flex space-x-4 max-w-xl';

  const avatar = document.createElement('img');
  avatar.src = botAvatar;
  avatar.alt = 'Bot avatar';
  avatar.className = 'rounded-full ml-3 w-8 h-8 object-cover border border-gray-200 shadow-sm flex-shrink-0'; 


  const messageBox = document.createElement('div');
  messageBox.className = 'bg-[#e9e8e3] rounded-xl p-6 text-[#0f3c4b] text-sm leading-relaxed max-w-[400px] break-words';
  messageBox.innerText = marked.parse(message);

  wrapper.appendChild(avatar);
  wrapper.appendChild(messageBox);

  return wrapper;
}

// Scroll chat to bottom
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userMessage = chatInput.value.trim();
  console.log("user msg" , userMessage)
  if (!userMessage) return;

  chatContainer.appendChild(createUserMessage(userMessage));
  scrollToBottom();
  chatInput.value = '';
  chatInput.disabled = true;

  try {
    const response = await fetch('api/ollama', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: userMessage }),
      mode: 'cors'
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    const botReply = data.response || data.error || 'Sorry, no reply.';
    chatContainer.appendChild(createBotMessage(botReply));
  } catch (err) {
    console.error('Error fetching bot response:', err);
    chatContainer.appendChild(createBotMessage('Oops! Something went wrong.'));
  } finally {
    scrollToBottom();
    chatInput.disabled = false;
    chatInput.focus();
  }
});

// Optionally, initialize with a welcome message from bot
chatContainer.appendChild(createBotMessage(
  "Hello! I'm your CATIA AI assistant. I can help you with CAD operations like generating bounding boxes, measuring parts, and analyzing your models."
));





// Backup code as of 5 Aug
// const chatContainer = document.getElementById('chat-container');
//   const chatForm = document.getElementById('chat-form');
//   const chatInput = document.getElementById('chat-input');

//   const userAvatar = "https://storage.googleapis.com/a1aa/image/759f54fa-e944-4d63-2afc-58cf0ca0a33b.jpg";
//   const botAvatar = "https://storage.googleapis.com/a1aa/image/274f13c7-ae6c-431b-7bfd-63c436fc4bef.jpg";

//   // Function to create user message div aligned right
//   function createUserMessage(message) {
//     const wrapper = document.createElement('div');
//     wrapper.className = 'flex justify-end max-w-xl';

//     const messageBox = document.createElement('div');
//     messageBox.className = 'bg-[#19707a] text-white rounded-xl px-6 py-4 text-sm leading-relaxed max-w-[400px] break-words';
//     messageBox.textContent = message;

//     const avatar = document.createElement('img');
//     avatar.src = userAvatar;
//     avatar.alt = 'User avatar';
//     avatar.className = 'rounded-full ml-3';
//     avatar.width = 32;
//     avatar.height = 32;

//     wrapper.appendChild(messageBox);
//     wrapper.appendChild(avatar);

//     return wrapper;
//   }

//   // Function to create bot message div aligned left
//   function createBotMessage(message) {
//     const wrapper = document.createElement('div');
//     wrapper.className = 'flex space-x-4 max-w-xl';

//     const avatar = document.createElement('img');
//     avatar.src = botAvatar;
//     avatar.alt = 'Bot avatar';
//     avatar.className = 'rounded-full flex-shrink-0';
//     avatar.width = 32;
//     avatar.height = 32;

//     const messageBox = document.createElement('div');
//     messageBox.className = 'bg-[#e9e8e3] rounded-xl p-6 text-[#0f3c4b] text-sm leading-relaxed max-w-[400px] break-words';
//     messageBox.textContent = message;

//     wrapper.appendChild(avatar);
//     wrapper.appendChild(messageBox);

//     return wrapper;
//   }

//   // Scroll chat to bottom
//   function scrollToBottom() {
//     chatContainer.scrollTop = chatContainer.scrollHeight;
//   }

//   chatForm.addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const userMessage = chatInput.value.trim();
//     if (!userMessage) return;

//     // Append user message
//     chatContainer.appendChild(createUserMessage(userMessage));
//     scrollToBottom();

//     // Clear input
//     chatInput.value = '';
//     chatInput.disabled = true;

//     try {
//       // Send POST request to your local Ollama LLM backend
//       // Adjust URL and request body as per your API design
//       const response = await fetch('http://localhost:5445/api/ollama', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ prompt: userMessage })
//       });

//       if (!response.ok) {
//         throw new Error(`Server error: ${response.status}`);
//       }

//       const data = await response.json();
//       const botReply = data.response || 'Sorry, I did not get that.';

//       // Append bot message
//       chatContainer.appendChild(createBotMessage(botReply));
//       scrollToBottom();
//     } catch (error) {
//       console.error('Error fetching bot response:', error);
//       chatContainer.appendChild(createBotMessage('Oops! Something went wrong.'));
//       scrollToBottom();
//     } finally {
//       chatInput.disabled = false;
//       chatInput.focus();
//     }
//   });

//   // Optionally, initialize with a welcome message from bot
//   chatContainer.appendChild(createBotMessage(
//     "Hello! I'm your CATIA AI assistant. I can help you with CAD operations like generating bounding boxes, measuring parts, and analyzing your models."
//   ));