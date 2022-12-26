import requests
from flask import Flask, request
import sqlite3
import configparser
import os


app = Flask(__name__)

# Check if the config.ini file exists
if not os.path.exists("config.ini"):
    # If the config.ini file does not exist, prompt for the Discord webhook URL and the port number
    discord_webhook_url = input("Enter the Discord webhook URL: ")
    port = input("Enter the port number: ")

    # Create the config.ini file
    config = configparser.ConfigParser()

    # Add the Discord webhook URL and port number to the config.ini file
    config["SECRETS"] = {"DISCORD_WEBHOOK_URL": discord_webhook_url}
    config["SETTINGS"] = {"PORT": port}

    # Write the config.ini file
    with open("config.ini", "w") as config_file:
        config.write(config_file)

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Get the Discord webhook URL and port number from the config.ini file
DISCORD_WEBHOOK_URL = config["SECRETS"]["DISCORD_WEBHOOK_URL"]
PORT = config["SETTINGS"]["PORT"]

@app.route('/', methods=['POST'])
def send_message_to_discord():
    # Connect to the database
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    # Create the messages table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, timestamp DATETIME, message TEXT)")

    # Get the request data
    data = request.get_json()

    # Iterate over the list of messages
    for message in data:
        # Extract the sender, message, and ID from the request data
        sender = message['sender']
        message_text = message['message']
        message_id = message['id']
        timestamp = message['timestamp']

        # Check if the message contains the "@" character
        if "@" in message_text:
            # If the message contains the "@" character, skip it
            continue

        # Check if the message ID has been seen before
        cursor.execute("SELECT * FROM messages WHERE id=?", (message_id,))
        if cursor.fetchone() is not None:
            # If the message ID has been seen before, skip it
            continue

        # Add the message ID and timestamp to the database
        cursor.execute("INSERT INTO messages (id, timestamp, message) VALUES (?, ?, ?)", (message_id, timestamp, message_text))
        conn.commit()

        # Format the message to send to Discord
        discord_message = f"{sender}: {message_text}"

        # Send the message to the Discord webhook
        requests.post(DISCORD_WEBHOOK_URL, json={'content': discord_message})

    # Close the database connection
    conn.close()

    return 'Messages sent to Discord successfully!'

if __name__ == '__main__':
    app.run(port=PORT)