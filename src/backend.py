import json
import os
import uuid

from dns import tokenizer
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import time
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DIR = os.path.join(BASE_DIR,'..','public','data')

# 确保聊天记录目录存在
os.makedirs(CHAT_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求


# 清理生成的文本（例如：去除多余字符）
def clean_generated_text(text: str) -> str:
    return text.strip()

# 调用 llama3.1 模型生成问题
def generate_question(content: str) -> str:
    prompt = content
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1"],
            input=prompt,
            capture_output=True, text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            question = result.stdout.strip()
            return clean_generated_text(question)
        else:
            print(f"Error generating question: {result.stderr}")
            return "Error generating question."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "Error generating question."

# 定义 Flask 路由来处理来自前端的请求
@app.route('/generate-question', methods=['POST'])
def handle_generate_question():
    data = request.get_json()
    user_message = data.get('content', '')

    if user_message:
        ai_question = generate_question(user_message)

        return jsonify({'question': ai_question}), 200
    else:
        return jsonify({'error': '无效输入'}), 400

def load_chat_history(user_id):
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat.json')
    try:
        with open(chat_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def save_chat_history(user_id, messages):
    # 使用当前时间戳生成唯一文件名
    timestamp = int(time.time())  # 获取当前秒级时间戳
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat_{timestamp}.json')
    with open(chat_file, 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)
@app.route('/Save', methods=['POST'])
def handle_save():
    data = request.get_json()

    if 'messages' not in data or not isinstance(data['messages'], list):
        return jsonify({'error': '消息格式不正确'}), 400


    messages = data['messages']
    if data['id'] == None:
        chat_id = str(uuid.uuid4())
    else:
        chat_id = data['id']
    chat_timestamp = messages[0]['timestamp']
    chat_name = "chat0101"
    chat_file_path = os.path.join(CHAT_DIR, f'{chat_id}.json')

    try:
        with open(chat_file_path, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)

        return jsonify({'status': '消息已保存'}), 200
    except Exception as e:

        return jsonify({'error': str(e)}), 500
def load_chat():
    chat_file_path = request.args.get('path')

    if not chat_file_path:
        return jsonify({'error': '缺少文件路径'}), 400

    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, '..', 'public', chat_file_path)

        if not os.path.isfile(full_path):
            return jsonify({'error': '聊天文件不存在'}), 404

        with open(full_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' not in data or not isinstance(data['messages'], list):
                return jsonify({'error': '消息格式不正确'}), 400

            return jsonify(data['messages'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


CORS(app)


@app.route('/Get_index', methods=['GET'])
# load index
def handle_get_index():

    chats = []
    for filename in os.listdir(CHAT_DIR):
        if filename.endswith('.json'):  # if json

            file_path = os.path.join(CHAT_DIR, filename)
            uuid, _ = os.path.splitext(filename)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)  # 读取 JSON 数据
                        timestamp = data['messages'][0]['timestamp']
                        chat = {
                            "uuid": uuid,
                            "name": data['messages'][0]['text'],
                            "timestamp": timestamp
                        }
                        chats.append(chat)
                    except json.JSONDecodeError:
                        print(f"文件 {filename} 不是有效的 JSON 格式。")
            else:
                print(f"文件 {filename} 不存在或为空。")
    return jsonify({'chats': chats}), 200



@app.route('/messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    messages = load_chat_history(user_id)
    return jsonify(messages), 200
# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)