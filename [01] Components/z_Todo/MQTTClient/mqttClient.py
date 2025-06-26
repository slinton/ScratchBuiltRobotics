import network
import time
import ubinascii
from umqtt.simple import MQTTClient

# WiFi Configuration
SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"

# MQTT Broker Configuration (HiveMQ public broker for testing)
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac')).decode()

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

# Callback function for receiving messages
def on_message(topic, msg):
    print(f"Received message on {topic}: {msg}")

# Connect to MQTT Broker
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.set_callback(on_message)
    client.connect()
    print("Connected to MQTT Broker")
    return client

# Main function
def main():
    connect_wifi()
    client = connect_mqtt()
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")
    
    while True:
        try:
            client.check_msg()  # Non-blocking check for new messages
            time.sleep(1)
            client.publish(MQTT_TOPIC, "Hello from MicroPython")
            print("Message published")
        except Exception as e:
            print("Error:", e)
            client.disconnect()
            time.sleep(5)
            main()

if __name__ == "__main__":
    main()
