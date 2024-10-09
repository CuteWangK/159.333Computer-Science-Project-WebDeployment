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
# 确保聊天记录目录存在
os.makedirs(CHAT_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求


# 清理生成的文本（例如：去除多余字符）
def clean_generated_text(text: str) -> str:
    return text.strip()

# 生成答案函数
def generate_answer(content: str) -> str:
    # 更新提示语，直接要求模型生成答案
    url = "http://localhost:4891/v1/chat/completions"

    # 设置请求数据
    payload = {
        "model": "unsloth.Q4_K_M",
        "messages": [
            {"role": "user",
             "content": f"{content}"}
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }

    # 设置请求头
    headers = {
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        # 生成答案，增加max_tokens长度以确保完整的答案
        json_response = response.json()
        # 提取并打印 message 里面的 content
        output = json_response['choices'][0]['message']['content']

        if output:  # 检查是否生成成功
            return output.strip()
            # answer = output["choices"][0]["text"].strip()
            # return clean_generated_text(answer)  # 清理生成的文本
        else:
            return "Error generating answer."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "Error generating answer."


# 处理前端生成答案请求的路由
@app.route('/generate-answer', methods=['POST'])
def handle_generate_answer():
    data = request.get_json()
    user_message = data.get('content', '')

    if user_message:
        ai_answer = generate_answer(user_message)
        return jsonify({'answer': ai_answer}), 200
    else:
        return jsonify({'error': 'Invalid input'}), 400


# 调用 llama3.1 模型生成问题
# def generate_question(content: str) -> str:
#     prompt = content
#     try:
#         result = subprocess.run(
#             ["ollama", "run", "llama3.1"],
#             input=prompt,
#             capture_output=True, text=True,
#             encoding='utf-8'
#         )
#         if result.returncode == 0:
#             question = result.stdout.strip()
#             return clean_generated_text(question)
#         else:
#             print(f"Error generating question: {result.stderr}")
#             return "Error generating question."
#     except Exception as e:
#         print(f"Exception occurred: {str(e)}")
#         return "Error generating question."
# 加载聊天历史
def load_chat_history(user_id):
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat.json')
    try:
        with open(chat_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' in data and isinstance(data['messages'], list):
                return data['messages']
            else:
                return []  # 如果 messages 为空或不存在，返回空列表
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"无法读取聊天记录: {user_id}")
        return []  # 如果文件不存在或无法解析，返回空列表


# 保存聊天历史
def save_chat_history(user_id, messages):
    chat_file = os.path.join(CHAT_DIR, f'{user_id}_chat.json')
    with open(chat_file, 'w', encoding='utf-8') as file:
        json.dump({"messages": messages}, file, ensure_ascii=False, indent=4)


# 处理聊天记录保存
@app.route('/Save', methods=['POST'])
def handle_save():
    data = request.get_json()

    if 'messages' not in data or not isinstance(data['messages'], list):
        return jsonify({'error': '消息格式不正确'}), 400

    messages = data['messages']
    chat_id = data.get('id', str(uuid.uuid4()))  # 使用 UUID 作为聊天 ID
    chat_file_path = os.path.join(CHAT_DIR, f'{chat_id}.json')

    try:
        with open(chat_file_path, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)
        return jsonify({'status': '消息已保存'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 加载聊天记录文件
@app.route('/load-chat', methods=['GET'])
def load_chat():
    chat_file_path = request.args.get('path')

    if not chat_file_path:
        return jsonify({'error': '缺少文件路径'}), 400

    try:
        full_path = os.path.join(CHAT_DIR, chat_file_path)

        if not os.path.isfile(full_path):
            return jsonify({'error': '聊天文件不存在'}), 404

        with open(full_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' not in data or not isinstance(data['messages'], list):
                return jsonify({'error': '消息格式不正确'}), 400
            return jsonify(data['messages'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 加载聊天索引列表
@app.route('/Get_index', methods=['GET'])
def handle_get_index():
    chats = []
    chat_counter = 1  # 初始化聊天计数器
    for filename in os.listdir(CHAT_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(CHAT_DIR, filename)
            uuid, _ = os.path.splitext(filename)  # 获取 UUID

            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        # 如果 messages 存在且不为空，则使用第一个消息，否则使用默认值
                        if 'messages' in data and len(data['messages']) > 0:
                            timestamp = data['messages'][0].get('timestamp', int(os.path.getctime(file_path)))
                            chat_name = f"New Chat {chat_counter}"
                        else:
                            # 当聊天记录为空时，使用递增的默认名称
                            timestamp = int(os.path.getctime(file_path))

                    except json.JSONDecodeError:
                        print(f"文件 {filename} 不是有效的 JSON 格式。")
                        continue
            else:
                # 文件为空时使用默认值
                timestamp = int(os.path.getctime(file_path))
                chat_name = f"New Chat {chat_counter}"

            chat = {
                "uuid": uuid,
                "name": chat_name,
                "timestamp": timestamp
            }
            chats.append(chat)
            chat_counter += 1  # 每次循环递增聊天计数器

    return jsonify({'chats': chats}), 200


files = {
    "66f92419-6ca8-8003-a696-8c67c0838e2c": {"title": "示例文件", "content": "这是与 UUID 关联的内容。"},
    # 其他文件...
}


@app.route('/chat/<uuid>', methods=['GET'])
def get_file(uuid):
    file_path = os.path.join(CHAT_DIR, f'{uuid}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "文件未找到"}), 404


# 删除聊天
@app.route('/DeleteChat', methods=['DELETE'])
def delete_chat():
    chat_id = request.args.get('id')

    if not chat_id:
        return jsonify({'error': '缺少聊天 ID'}), 400

    chat_file_path = os.path.join(CHAT_DIR, f'{chat_id}.json')

    if os.path.exists(chat_file_path):
        try:
            os.remove(chat_file_path)
            return jsonify({'status': '聊天已删除'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': '聊天记录不存在'}), 404


# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
