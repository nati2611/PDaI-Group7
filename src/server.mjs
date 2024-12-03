//import fs from 'fs';

// Der Text, den wir in die Datei schreiben möchten
/*const message = "Dies ist eine Nachricht, die in die Datei geschrieben wird.\n";

function write(text){
    fs.appendFile('chat.txt', text, (err) => {
        if (err) {
        console.error('Fehler beim Schreiben der Datei:', err);
        } else {
        console.log('Nachricht erfolgreich in die Datei geschrieben!');
        }
    });
} */


    import WebSocket, { WebSocketServer } from "ws";

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you're trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

const wss = new WebSocketServer({ port: 3000 });

wss.on("connection", function connection(ws) {
  ws.on("message", function message(message) {
    const data = JSON.parse(message);

    if (data.type === "message") {
      // Broadcast user message to other clients
      wss.clients.forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: "message", data: data.data }));
        }
      });

      // Respond as the bot
      const botMessage = BOT_MSGS[Math.floor(Math.random() * BOT_MSGS.length)];
      ws.send(JSON.stringify({ type: "message", data: botMessage }));
    }
  });
});


/*import express from 'express';
import { Server } from 'http';
import { Server as SocketIOServer } from 'socket.io';

const app = express();
const http = new Server(app);
const io = new SocketIOServer(http);
    

io.on('connection', function(socket) {
  console.log('A user connected.');

  // Handle incoming messages from clients
  socket.on('message', function(message) {
    console.log('Message received:', message);

    // Broadcast the message to all connected clients
    io.emit('message', message);
  });

  // Handle disconnection
  socket.on('disconnect', function() {
    console.log('A user disconnected.');
  });
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, function() {
  console.log(`Server listening on port ${PORT}`);
}); 
*/

/*import { createServer } from 'node:http';

const hostname = '127.0.0.1';
const port = 3000;

const server = createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
*/