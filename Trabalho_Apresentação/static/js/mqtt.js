// Configurações MQTT
const clientId = `clientId-${Math.random().toString(16).slice(2)}`;
const host = 'mqtt-dashboard.com';
const port = 8884; // Porta SSL
const topic = 'exp-sensor-rodrigo';

// Cliente MQTT
const client = new Paho.MQTT.Client(host, port, `/mqtt`, clientId);

client.onConnectionLost = responseObject => {
    console.log("Conexão perdida: " + responseObject.errorMessage);
    setTimeout(() => { client.connect(connectOptions); }, 5000); // Reconecta após 5 segundos
};

client.onMessageArrived = message => {
    console.log("Mensagem recebida: " + message.payloadString);
    displayMessage(message.payloadString);
    sendMessageToServer(message.payloadString);
};

const connectOptions = {
    useSSL: true,
    timeout: 3,
    onSuccess: () => {
        console.log("Conectado ao broker MQTT.");
        client.subscribe(topic);
    },
    onFailure: (error) => {
        console.log("Falha na conexão: " + error.errorMessage);
        setTimeout(() => { client.connect(connectOptions); }, 5000); // Reconecta após 5 segundos
    }
};

client.connect(connectOptions);

function displayMessage(msg) {
    const messagesList = document.getElementById('messagesList');
    const newMessage = document.createElement('li');
    newMessage.textContent = msg;
    messagesList.appendChild(newMessage);
}

function sendMessageToServer(msg) {
    fetch('/save_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: msg, topic: topic })
    })
    .then(response => response.json())
    .then(data => console.log('Message saved:', data))
    .catch((error) => {
        console.error('Error:', error);
    });
}
