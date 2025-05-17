# decision.py
import paho.mqtt.client as mqtt
import json

def decide(detections):
    # Αν υπάρχουν περισσότερα από 3 αντικείμενα → alert
    return len(detections) > 3

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    dets = data.get('detections', [])
    if decide(dets):
        alert = json.dumps({
            'drone_id': data.get('drone_id'),
            'alert': True
        })
        client.publish('swarm/alerts', alert)
        print(f"[ALERT] Drone {data.get('drone_id')} sent an alert!")

client = mqtt.Client()
client.on_message = on_message
client.connect('localhost')
client.subscribe('swarm/detections')
client.loop_forever()
