import fs from 'fs';

// Der Text, den wir in die Datei schreiben möchten
const message = "Dies ist eine Nachricht, die in die Datei geschrieben wird.\n";

function write(text){
    fs.appendFile('chat.txt', text, (err) => {
        if (err) {
        console.error('Fehler beim Schreiben der Datei:', err);
        } else {
        console.log('Nachricht erfolgreich in die Datei geschrieben!');
        }
    });
}