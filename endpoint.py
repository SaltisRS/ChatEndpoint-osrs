import requests
from flask import Flask, request

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1033490255950663710/PMenNborc711bQ2ttQCUoaHFLwSa60oNa6Pz6fWUoo6gna2hBdFDRtHI-cUavZ9rlwmS"
@app.route('/', methods=['POST'])
def send_message_to_discord():
    # Get the request data
    data = request.get_json()

    # Iterate over the list of messages
    for message in data:
        # Extract the sender and message from the request data
        sender = message['sender']
        message_text = message['message']

        # Format the message to send to Discord
        discord_message = f"{sender}: {message_text}"

        # Send the message to the Discord webhook
        requests.post(DISCORD_WEBHOOK_URL, json={'content': discord_message})

    return 'Messages sent to Discord successfully!'

if __name__ == '__main__':
    app.run()