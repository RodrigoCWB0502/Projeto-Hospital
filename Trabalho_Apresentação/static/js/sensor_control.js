document.addEventListener("DOMContentLoaded", function() {
    var client;
    var isConnected = false;

    function MQTTconnect() {
        client = new Paho.MQTT.Client("mqtt-dashboard.com", 8000, "sensor-exp-criativa-rodrigo");
        var options = {
            timeout: 3,
            onSuccess: onConnect,
            onFailure: onFailure,
            userName: "",
            password: "",
            useSSL: false,
            cleanSession: true,
        };
        client.onConnectionLost = onConnectionLost;
        client.connect(options);
    }

    function onConnect() {
        console.log("MQTT connected");
        isConnected = true;
        client.subscribe("exp-sensor-rodrigo");
    }

    function onFailure(message) {
        console.log("Connection failed: " + message.errorMessage);
        isConnected = false;
        setTimeout(MQTTconnect, 5000);
    }

    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("Connection lost: " + responseObject.errorMessage);
            isConnected = false;
            setTimeout(MQTTconnect, 5000);
        }
    }

    function sendMQTTMessage(action) {
        if (isConnected) {
            var message = new Paho.MQTT.Message(action);
            message.destinationName = "exp-sensor-rodrigo";
            client.send(message);
            sendMessageToServer(action); // Call to send data to Flask server
        } else {
            console.log("Not connected to MQTT.");
            MQTTconnect();
        }
    }

    function sendMessageToServer(action) {
        fetch('/save_event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event_type: action })
        }).then(response => response.json())
          .then(data => console.log('Event saved:', data))
          .catch(error => console.error('Error:', error));
    }

    window.onload = MQTTconnect;

    document.getElementById('activateSensor').addEventListener('click', function() {
        sendMQTTMessage('ON');
    });

    document.getElementById('deactivateSensor').addEventListener('click', function() {
        sendMQTTMessage('OFF');
    });
});
