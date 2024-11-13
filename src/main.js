const chatform = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput");
const chatDisplay = document.getElementById("chatDisplay");

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
        </br>
    </div>
  `;

  chatDisplay.insertAdjacentHTML("beforeend", msgHTML);
  chatDisplay.scrollTop = chatDisplay.scrollHeight;
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