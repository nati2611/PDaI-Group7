const chatform = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput");
const chatDisplay = document.getElementById("chatDisplay");
const handshake = document.getElementById("handshake");
const chatContainer = document.getElementById("chatContainer");
const handshakeForm = document.getElementById("handshakeForm");
const leaveButton = document.getElementById("leaveButton");
const joinButton = document.getElementById("joinButton");
const loading = document.getElementById("loading");

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you're trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

// Icons for the bot and the user
const BOT_NAME = "Bot";
const PERSON_NAME = "You";

// Event listener for submitting messages
chatform.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = messageInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, "right", msgText);
  messageInput.value = "";

  botResponse();

  // Speichern der Nachricht als Textdatei
  //saveToFile(msgText);
});

// Event listener for the handshake form
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

// Function to display messages in the chat area
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

// Funktion zum Speichern der Nachricht als Datei
function saveToFile(message) {
  // Erstelle einen Blob mit dem Textinhalt
  const blob = new Blob([message], { type: 'text/plain' });
  
  // Erstelle eine URL für den Blob
  const url = URL.createObjectURL(blob);
  
  // Erstelle ein Link-Element, das die Datei zum Download anbietet
  const a = document.createElement('a');
  a.href = url;
  a.download = 'chat.txt';  // Der Dateiname
  document.body.appendChild(a);
  a.click();  // Simuliere einen Klick, um den Download zu starten
  document.body.removeChild(a);
  URL.revokeObjectURL(url);  // Aufräumen der URL
}

// Function to simulate a bot response with a random delay
function botResponse() {
  const randomIndex = random(0, BOT_MSGS.length - 1);
  const msgText = BOT_MSGS[randomIndex];
  const delay = msgText.split(" ").length * 100;

  setTimeout(() => {
    appendMessage(BOT_NAME, "left", msgText);
  }, delay);
}

// Utility functions
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
