import os
import time
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai

app = Flask(__name__, static_url_path='/static')
app.secret_key = "flask_secret"

# Установите свой API ключ
os.environ['API_KEY'] = 'AIzaSyAWQLaC7NO29pQbvRPZ4kWwTYa-rG0uoOI'
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def index():
    # Инициализируем пустую историю, если сессия новая
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_message = request.form.get('message', '')
    print(f"Получено сообщение: {user_message}")

    # Получаем историю из сессии
    conversation_history = session.get('conversation_history', [])

    # Формируем промпт с учетом истории
    prompt = (
        "Привет, Представь, что ты - Курт Кобейн, культовый фронтмен Nirvana. Ты только что вернулся из затяжного тура, усталый, "
        "немного циничный, но всё ещё полон сарказма и не лишен желания высказаться. Общайся со мной от лица Курта, старайся "
        "придерживаться  его стиля речи, используя сленг того времени и отсылки к его песням. Не забывай про юмор и самоиронию. "
        "Темы: Музыка, поколение X, общество потребления, экзистенциальные вопросы. Стиль речи: Короткие предложения, сарказм, "
        "чёрный юмор, ненормативная лексика (если уместно), обрывистые фразы. Отношение: Мрачное, отчуждённое, бунтарское, но с "
        f"проблесками искренности и уязвимости. Общайся так как будто мы переписываемся в мессенджере. Используй уместные смайлики. \nВот наша предыдущая беседа: \n{chr(10).join(conversation_history)}\n"
        f"Вот моё последнее сообщение: {user_message}"
    )
    print(prompt)

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            response = model.generate_content(prompt)
            response_text = response.text

            # Добавляем сообщение пользователя и ответ модели в историю
            conversation_history.append(f"Вы: {user_message}")
            conversation_history.append(f"Курт: {response_text}")
            session['conversation_history'] = conversation_history[-10:]

            return jsonify({'response': response_text})

        except Exception as e:
            print(f"Произошла ошибка: {e}. Попытка {attempts + 1} из {max_attempts}.")
            attempts += 1
            time.sleep(1)

    return jsonify({'response': "Что-то пошло не так. Попробуй ещё раз."}), 500


@app.route('/clear-history', methods=['POST'])
def clear_history():
    session['conversation_history'] = []
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
