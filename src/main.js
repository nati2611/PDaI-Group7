const chatform = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput");
const chatDisplay = document.getElementById("chatDisplay");
const handshake = document.getElementById("handshake");
const chatContainer = document.getElementById("chatContainer");
const handshakeForm = document.getElementById("handshakeForm");
const leaveButton = document.getElementById("leaveButton");
const joinButton = document.getElementById("joinButton");
const loading = document.getElementById("loading");

const BOT_NAME = "Bot";
const PERSON_NAME = "You";
const ws = new WebSocket('ws://localhost:3000'); // Updated port

ws.onmessage = (event) => {
  const { type, data } = JSON.parse(event.data);
  if (type === "message") {
    appendMessage(BOT_NAME, "left", data); // Display bot's response
  }
};

// Event listener for submitting messages
chatform.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = messageInput.value;
  if (!msgText) return;

  ws.send(JSON.stringify({ type: "message", data: msgText })); // Send message to server
  appendMessage(PERSON_NAME, "right", msgText);
  messageInput.value = "";
});

handshakeForm.addEventListener("submit", async event => {
  event.preventDefault();

  // Show the loading element
  loading.classList.remove("hidden");
  joinButton.classList.add("hidden");

  loading.innerHTML = `<img src='https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmV6NzBtZnNjeXRkZzY4ZXlhdzJnazZnZzRtcGl2YzJrejA3aDJ1dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MDrmyLuEV8XFOe7lU6/giphy.gif'  
    alt='Loading...' style='width:90%' />`;

  // Delay for 5 seconds
  setTimeout(() => {
    // Hide handshake and loading screen
    handshake.classList.add("hidden");
    loading.classList.add("hidden");

    // Show chat container
    chatContainer.classList.remove("hidden");
    leaveButton.classList.remove("hidden");

    // Add welcome message
    appendMessage(BOT_NAME, "left", "Hello " + name + "! How can I help you today?");
  }, 5000);
});


leaveButton.addEventListener("click", () => {
  chatContainer.classList.add("hidden");
  handshake.classList.remove("hidden");
  leaveButton.classList.add("hidden");
  joinButton.classList.remove("hidden");
  chatDisplay.innerHTML = "";
});

function appendMessage(name, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
    </div>
  `;

  chatDisplay.insertAdjacentHTML("beforeend", msgHTML);
  chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// Utility function
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}
