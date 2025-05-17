# comm.py
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    count = len(data.get('detections', []))
    print(f"[MSG] From Drone {data.get('drone_id')}: {count} detections")

client = mqtt.Client()
client.on_message = on_message
client.connect('localhost')
client.subscribe('swarm/detections')
client.loop_forever()
