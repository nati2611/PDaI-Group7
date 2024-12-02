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

/*const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

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
}); */

import { createServer } from 'node:http';

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
