const chatform = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput");
const chatDisplay = document.getElementById("chatDisplay");
const typingIndicator = document.getElementById("typingIndicator"); // Add an element for showing typing
const handshake = document.getElementById("handshake");
const chatContainer = document.getElementById("chatContainer");
const handshakeForm = document.getElementById("handshakeForm");
const leaveButton = document.getElementById("leaveButton");
const joinButton = document.getElementById("joinButton");
const loading = document.getElementById("loading");
const client1_name = "You"; // Your client's name
const client2_name = "Other client"; // Other clients' name
const ws = new WebSocket("ws://localhost:3000");

let typingTimeout;

// Event listener for incoming WebSocket messages
ws.onmessage = (event) => {
  const { type, data, user } = JSON.parse(event.data);

  if (type === "message") {
    // Determine sender name based on the user field
    const senderName = user === client1_name ? client1_name : client2_name;
    const messageSide = senderName === client1_name ? "right" : "left";
    appendMessage(senderName, messageSide, data);
  } else if (type === "typing") {
    showTypingIndicator(user);
  }
};

// Event listener for submitting messages
chatform.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = messageInput.value;
  if (!msgText) return;

  ws.send(JSON.stringify({ type: "message", data: msgText, user: client1_name }));
  appendMessage(client1_name, "right", msgText);
  messageInput.value = "";
});

// Event listener for input changes to detect typing
messageInput.addEventListener("input", () => {
  ws.send(JSON.stringify({ type: "typing", user: client1_name })); // Notify server of typing
  clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    ws.send(JSON.stringify({ type: "typing", user: null })); // Clear typing indicator after timeout
  }, 1000);
});

// Handshake join form submission
handshakeForm.addEventListener("submit", async (event) => {
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
    appendMessage(client2_name, "left", "Hello! How can I help you today?");
  }, 5000);
});

// Leave button logic
leaveButton.addEventListener("click", () => {
  chatContainer.classList.add("hidden");
  handshake.classList.remove("hidden");
  leaveButton.classList.add("hidden");
  joinButton.classList.remove("hidden");
  chatDisplay.innerHTML = "";
});

// Function to display typing indicator
function showTypingIndicator(user) {
  if (user) {
    typingIndicator.textContent = `${user} is typing...`;
  } else {
    typingIndicator.textContent = "";
  }
}

// Function to append chat messages
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

// Utility function to format the date
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}
