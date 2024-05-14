from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import asyncio
from hume import HumeVoiceClient, MicrophoneInterface
from hume import VoiceConfig, HumeVoiceClient
from dotenv import load_dotenv
import os
import sys

load_dotenv()

app = Flask(__name__)
program_running = True
socketio = SocketIO(app)


@app.route('/check_status', methods=['GET'])
def check_status():
    return jsonify({'running': program_running})

# Initialize the HumeVoiceClient
hume_api_key = os.environ.get("HUME_API_KEY")
client = HumeVoiceClient(hume_api_key)  # Initialize client using the API key

@socketio.on('chat_message')
def handle_chat_message(data):
    emit('chat_message', data, broadcast=True)

# Define the list_configs function outside the main loop
def display_configs():
    configs = [(config.name, config.id) for config in client.iter_configs()]
    return configs


# Define function to delete a personality configuration
def delete_personality_config(config_id):
    client.delete_config(config_id)


# def create_personality_config(client):
#     name = input("Enter the personality name: ")
#     prompt = input("Enter the prompt: ")
#     config: VoiceConfig = client.create_config(
#         name=name,
#         prompt=prompt,
#     )
#     print("Created config:", config.id)

# Define function to create a personality configuration
def create_personality_config(name, prompt):
    config = client.create_config(name=name, prompt=prompt)
    return config.id


def list_configs(client):
    configs = [(config.name, config.id) for config in client.iter_configs()]
    for index, (name, config_id) in enumerate(configs, start=1):
        print(f"{index}. {name} ({config_id})")

    while True:
        choice = input("Enter the number of the configuration you want to use: ")
        try:
            choice_index = int(choice)
            if 1 <= choice_index <= len(configs):
                selected_config_name, selected_config_id = configs[
                    choice_index - 1]  # Get the selected config (name, id)
                return selected_config_name, selected_config_id
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


chat_active = True

@app.route("/stop_chat", methods=["POST"])
def stop_chat():
    global chat_active
    chat_active = False  # Set the flag to indicate that the chat session should be terminated
    return jsonify(success=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        choice = data.get("choice")
        if choice == "1":
            global chat_active
            chat_active = True  # Set the flag to indicate that the chat session is active

            async def talk_baymax():
                async with client.connect(config_id="6aa1a7ca-d3d0-4ea9-9e7d-97b064e7c109") as socket:
                    while chat_active:  # Check if the chat session is active
                        await MicrophoneInterface.start(socket)

            asyncio.run(talk_baymax())
            chat_active = False
        elif choice == "2":
            config_id = data.get("config")
            configs = display_configs()
            # return jsonify(configs=configs)
            return jsonify(success=True)
        elif choice == "3":
            # Create personality configuration
            name = data.get("personalityName")
            prompt = data.get("personalityDescription")
            config_id = create_personality_config(name, prompt)
            return jsonify(success=True, config_id=config_id)
        elif choice == "4":
            config_id = data.get("deleteConfig")
            delete_personality_config(config_id)
            return jsonify(success=True)
        else:
            return "Invalid choice. Please choose again."

    configs = display_configs()  # Get the configs for the initial load
    return render_template("index.html", configs=configs)


if __name__ == "__main__":
    app.run(debug=True)