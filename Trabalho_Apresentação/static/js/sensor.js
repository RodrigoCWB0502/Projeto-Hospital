const clientId = `clientId-${Math.random().toString(16).slice(2)}`; // Cliente ID
const host = 'mqtt-dashboard.com';
const port = 8884; // Porta SSL
const topic = 'exp-sensor-rodrigo';

const client = new Paho.MQTT.Client(host, port, `/mqtt`, clientId);

client.onConnectionLost = responseObject => {
    console.log("Conexão perdida: " + responseObject.errorMessage);
    setTimeout(() => { client.connect(options); }, 5000); // Reconecta dps de 5 seg
};

client.onMessageArrived = message => {
    console.log("Mensagem recebida: " + message.payloadString);
    displayMessage(message.payloadString);
};

const options = {
    useSSL: true,
    timeout: 3,
    onSuccess: () => {
        console.log("Conectado ao broker MQTT.");
        client.subscribe(topic);
    },
    onFailure: (error) => {
        console.log("Falha na conexão: " + error.errorMessage);
        setTimeout(() => { client.connect(options); }, 5000); // Reconecta dps de 5 seg
    }
};

client.connect(options);

function displayMessage(msg) {
    const messagesList = document.getElementById('messagesList');
    const newMessage = document.createElement('li');
    newMessage.textContent = msg;
    messagesList.appendChild(newMessage);
}
