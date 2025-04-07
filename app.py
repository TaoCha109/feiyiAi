
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
DEEPSEEK_API_KEY = ""
API_URL = ""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ai')
def ai_chat():
    return render_template('ai_chat.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/train')
def train():
    return render_template('train.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个非物质文化遗产专家，请用中文回答相关问题"},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        result = response.json()

        # 更健壮的错误处理
        if 'choices' not in result or not result['choices']:
            return jsonify({"error": "返回格式异常"}), 500

        return jsonify({
            "reply": result['choices'][0]['message']['content']
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"请求失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)