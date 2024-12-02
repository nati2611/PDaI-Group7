const ws = new WebSocket('ws://localhost:3000');

ws.addEventListener("message", function(event) {
    const data = JSON.parse(event.data);

    if (data.type === "message") { //status also possible etc
        appendMessage(data.data, "left", data.text);
    }

  console.log('Message from server:', event.data);
});

function sendMessage(message) {
    const message = document.getElementById("messageInput").value;
    if (!message) return false; //nothing happens when the button is clicked

    ws.send(JSON.stringify({ type: "message", data: message }));

    addMessage(message);

    document.getElementById("messageInput").value = "";
}

function addMessage(message) {
    const node = document.createElement("div");
    const text = document.createTextNode(message);

    node.appendChild(text);
    node.classList.add("msg", "right-msg");

    document.getElementById("chatDisplay").appendChild(node);
    

}