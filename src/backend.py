import json
import os
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

    chat_id = data['id']
    messages = data['messages']
    chat_file_path = os.path.join(CHAT_DIR, f'chat{chat_id}.json')

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

@app.route('/messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    messages = load_chat_history(user_id)
    return jsonify(messages), 200
# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
