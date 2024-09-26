from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

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
    data = request.json
    content = data.get('content', '')

    if not content:
        return jsonify({"error": "No content provided"}), 400

    question = generate_question(content)
    return jsonify({"question": question})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
