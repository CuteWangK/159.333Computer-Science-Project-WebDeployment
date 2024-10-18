import json
import os
import uuid
import subprocess
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DIR = os.path.join(BASE_DIR, '..', 'public', 'data')
import requests

# Make sure the chat log directory exists
os.makedirs(CHAT_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from all sources

# Cleaning up the generated text (e.g., removing redundant characters)
def clean_generated_text(text: str) -> str:
    return text.strip()

# Generate Answer Function
def generate_answer(content: str) -> str:
    url = "http://localhost:4891/v1/chat/completions"

    # Setting request data
    payload = {
        "model": "unsloth.Q4_K_M",
        "messages": [
            {"role": "user",
             "content": f"{content}"}
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }

    # Setting the request header
    headers = {
        "Content-Type": "application/json"
    }

    # Send a POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        # Generate answers, increase max_tokens length to ensure complete answers
        json_response = response.json()
        # Extracts and prints the content inside the message
        output = json_response['choices'][0]['message']['content']

        if output:  # Check for successful generation
            return output.strip()
        else:
            return "Error generating answer."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "Error generating answer."

# Routes that handle front-end requests to generate answers
@app.route('/generate-answer', methods=['POST'])
def handle_generate_answer():
    data = request.get_json()
    user_message = data.get('content', '')

    if user_message:
        ai_answer = generate_answer(user_message)
        return jsonify({'answer': ai_answer}), 200
    else:
        return jsonify({'error': 'Invalid input'}), 400

# Load Chat History
def load_chat_history(user_id):
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat.json')
    try:
        with open(chat_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' in data and isinstance(data['messages'], list):
                return data['messages']
            else:
                return []  # Returns an empty list if messages is empty or does not exist.
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Unable to read chat logs: {user_id}")
        return []  # Returns an empty list if the file does not exist or cannot be parsed

# Save Chat History
def save_chat_history(user_id, messages):
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat.json')
    with open(chat_file, 'w', encoding='utf-8') as file:
        json.dump({"messages": messages}, file, ensure_ascii=False, indent=4)

# Handle saving chat logs
@app.route('/Save', methods=['POST'])
def handle_save():
    data = request.get_json()

    if 'messages' not in data or not isinstance(data['messages'], list):
        return jsonify({'error': 'Incorrect message format'}), 400

    messages = data['messages']
    chat_id = data.get('id', str(uuid.uuid4()))  # Using UUID as Chat ID
    chat_file_path = os.path.join(CHAT_DIR, f'{chat_id}.json')

    try:
        with open(chat_file_path, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)
        return jsonify({'status': 'Message saved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Load chat log file
@app.route('/load-chat', methods=['GET'])
def load_chat():
    chat_file_path = request.args.get('path')

    if not chat_file_path:
        return jsonify({'error': 'Missing file path'}), 400

    try:
        full_path = os.path.join(CHAT_DIR, chat_file_path)

        if not os.path.isfile(full_path):
            return jsonify({'error': 'Chat file does not exist'}), 404

        with open(full_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' not in data or not isinstance(data['messages'], list):
                return jsonify({'error': 'Incorrect message format'}), 400
            return jsonify(data['messages'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Load Chat Index List
@app.route('/Get_index', methods=['GET'])
def handle_get_index():
    chats = []
    chat_counter = 1  # Initialize chat counter
    for filename in os.listdir(CHAT_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(CHAT_DIR, filename)
            uuid, _ = os.path.splitext(filename)  # Get UUID

            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        # If messages exist and are not empty, use the first message, otherwise use default
                        if 'messages' in data and len(data['messages']) > 0:
                            timestamp = data['messages'][0].get('timestamp', int(os.path.getctime(file_path)))
                            chat_name = "New Chat"
                        else:
                            # When chat history is empty, use incrementing default name
                            timestamp = int(os.path.getctime(file_path))

                    except json.JSONDecodeError:
                        print(f"File {filename} is not a valid JSON format.")
                        continue
            else:
                # When the file is empty, use default values
                timestamp = int(os.path.getctime(file_path))
                chat_name = f"New Chat {chat_counter}"

            chat = {
                "uuid": uuid,
                "name": chat_name,
                "timestamp": timestamp
            }
            chats.append(chat)
            chat_counter += 1  # Increment chat counter with each loop

    return jsonify({'chats': chats}), 200

files = {
    "66f92419-6ca8-8003-a696-8c67c0838e2c": {"title": "Example File", "content": "This is content associated with the UUID."},
    # Other files...
}

@app.route('/chat/<uuid>', methods=['GET'])
def get_file(uuid):
    file_path = os.path.join(CHAT_DIR, f'{uuid}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "File not found"}), 404

# Delete Chat
@app.route('/DeleteChat', methods=['DELETE'])
def delete_chat():
    chat_id = request.args.get('id')

    if not chat_id:
        return jsonify({'error': 'Missing chat ID'}), 400

    chat_file_path = os.path.join(CHAT_DIR, f'{chat_id}.json')

    if os.path.exists(chat_file_path):
        try:
            os.remove(chat_file_path)
            return jsonify({'status': 'Chat deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Chat record does not exist'}), 404

# Start Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
