import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Подгружаем переменные окружения из .env (в первую очередь SECRET_KEY)
load_dotenv()

app = Flask(__name__)
# Секретный ключ берём из окружения. Значение по умолчанию — только для локальной отладки.
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

def load_digest_data():
    """Загружает список нейросетей из JSON-файла-базы данных"""
    json_path = os.path.join(app.root_path, 'data.json')
    
    # Если файла еще нет или он пустой, отдаем базовый каркас для теста
    if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        default_data = [
            {
                "id": 1,
                "title": "Telegram-бот @amazo_first_bot",
                "desc": "Коммерческий MVP-ассистент для автоматизации бизнес-процессов на заказ.",
                "tag": "bots",
                "tag_name": "Боты",
                "cpa_url": "https://t.me",
                "affiliate_url": "",
                "erid": ""
            },
            {
                "id": 2,
                "title": "Генератор Glassmorphism",
                "desc": "Инструмент для создания космических CSS-эффектов матового стекла.",
                "tag": "design",
                "tag_name": "Дизайн",
                "cpa_url": "#",
                "affiliate_url": "",
                "erid": ""
            }
        ]
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    # Загружаем динамические карточки из data.json
    cards = load_digest_data()

    # Считаем общее количество для нашего JS-счетчика
    total_cards = len(cards)

    # Собираем список категорий для кнопок-фильтров (без дублей, в порядке карточек)
    tag_names = []
    for card in cards:
        name = card.get("tag_name") or card.get("tag")
        if name and name not in tag_names:
            tag_names.append(name)

    return render_template(
        'index.html',
        cards=cards,
        total_cards=total_cards,
        tag_names=tag_names
    )

if __name__ == '__main__':
    app.run(debug=True)
