from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1033490255950663710/PMenNborc711bQ2ttQCUoaHFLwSa60oNa6Pz6fWUoo6gna2hBdFDRtHI-cUavZ9rlwmS"

@app.route("/send_message", methods=["POST"])
def send_message():
    # Get the message to be sent from the request data
    data = request.get_json()
    message = data["message"]
    
    # Send a request to the Discord webhook with the message
    requests.post(DISCORD_WEBHOOK_URL, json={
        "content": message
    })
    
    return "Message sent to Discord!"

if __name__ == "__main__":
    app.run()