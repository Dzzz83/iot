import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, CallbackAPIVersion
import json
import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

# initialize counterfit connection
CounterFitConnection.init('127.0.0.1', 5000)

# setup virtual hardware
light_sensor = GroveLightSensor(0)
led = GroveLed(1)

# device info
id = '00c3d273-3908-4abc-bf49-da05232ec820'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_combined'

# create mqtt client
mqtt_client = Client(client_id=client_name, callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("mqtt connected!")

# send light sensor data
def send_telemetry():
    light_value = light_sensor.light
    telemetry = json.dumps({'light': light_value})
    print("sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

# process received telemetry
def receive_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("telemetry received:", payload)
    return payload

# send led control command
def send_commands(command):
    command_json = json.dumps(command)
    print("sending command:", command_json)
    mqtt_client.publish(server_command_topic, command_json)

# process received commands
def get_commands(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("command received:", payload)
    if payload.get('led_on'):
        led.on()
        print("led turned on")
    else:
        led.off()
        print("led turned off")

# handle incoming messages
def on_message(client, userdata, message):
    if message.topic == client_telemetry_topic:
        payload = receive_telemetry(client, userdata, message)
        command = {'led_on': payload.get('light', 0) < 300}  # turn led on if light < 300
        send_commands(command)
    elif message.topic == server_command_topic:
        get_commands(client, userdata, message)

mqtt_client.on_message = on_message

# subscribe to topics
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.subscribe(server_command_topic)

# main loop
try:
    while True:
        send_telemetry()
        time.sleep(5)
except KeyboardInterrupt:
    print("\ndisconnecting...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("disconnected gracefully.")
