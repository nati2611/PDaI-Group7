import WebSocket, { WebSocketServer } from "ws";

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you're trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

const wss = new WebSocketServer({ port: 3000 });

wss.on("connection", (ws) => {
  ws.on("message", (message) => {
    const data = JSON.parse(message);

    if (data.type === "message") {
      // Broadcast user message to other clients
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: "message", data: data.data, user: data.user }));
        }
      });

      // Respond as the bot
      const botMessage = BOT_MSGS[Math.floor(Math.random() * BOT_MSGS.length)];
      ws.send(JSON.stringify({ type: "message", data: botMessage, user: "Bot" }));
    } else if (data.type === "typing") {
      // Broadcast typing status to other clients
      wss.clients.forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: "typing", user: data.user }));
        }
      });
    }
  });
});
