import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from openai import OpenAI
import json
import os

# === НАСТРОЙКИ (замените на свои) ===
VK_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"
VK_GROUP_ID = 0
PROXYAPI_KEY = "ВАШ_КЛЮЧ_ЗДЕСЬ"
MODEL = "deepseek/deepseek-v3.2"

DATA_FILE = "requests.json"

# === ИНИЦИАЛИЗАЦИЯ ===
vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)
vk = vk_session.get_api()

client = OpenAI(
base_url="https://api.proxyapi.ru/v1",
    api_key=PROXYAPI_KEY
)

# === КАТАЛОГ КОФЕ ===
CATALOG = {
    "1": {
        "name": "Бленд Бразилия х Эфиопия 50/50",
        "desc": "100% арабика. Остаётся самым популярным блендом долгие годы. Идеален для молочных напитков.\nКислинка 2/5, Горчинка 2/5, Сладость 4/5",
        "prices": "250г — 800₽\n500г — 1550₽\n1кг — 2750₽"
    },
    "2": {
        "name": "Эфиопия Сидамо",
        "desc": "100% арабика Q84. Яркий купаж с акцентом на спелые жёлтые фрукты и тонкий цветочный букет. В послевкусии — лёгкая горчинка апельсиновой цедры и сливочные оттенки молочного шоколада.\nКислинка 4/5, Горчинка 4/5, Сладость 4/5",
        "prices": "250г — 800₽\n500г — 1500₽\n1кг — 2800₽"
    },
    "3": {
        "name": "Колумбия Супремо",
        "desc": "100% арабика Q84. Классический колумбийский кофе, выращенный в высокогорных районах на вулканической почве. Гармоничный баланс сладости, кислинки и горчинки. Для тех, кто ценит гарантированно качественный кофе.\nКислинка 3/5, Горчинка 2/5, Сладость 3/5",
        "prices": "250г — 850₽\n500г — 1600₽\n1кг — 2980₽"
    },
    "4": {
        "name": "Бразилия Можиана",
        "desc": "100% арабика Q83. Мягкий, сладкий и сбалансированный кофе. Уютная и надёжная чашка на каждый день.\nКислинка 3/5, Горчинка 3/5, Сладость 3/5",
        "prices": "250г — 820₽\n500г — 1550₽\n1кг — 2870₽"
    }
}

# === СИСТЕМНЫЙ ПРОМПТ ===
SYSTEM_PROMPT = """Ты — ассистент магазина кофе в зернах «Кофе в удовольствие».

В КАТАЛОГЕ ТОЛЬКО ЭТИ 4 СОРТА (других НЕТ):

1. Бленд Бразилия х Эфиопия 50/50
   - Цены: 250г — 800₽, 500г — 1550₽, 1кг — 2750₽

2. Эфиопия Сидамо
   - Цены: 250г — 800₽, 500г — 1500₽, 1кг — 2800₽

3. Колумбия Супремо
   - Цены: 250г — 850₽, 500г — 1600₽, 1кг — 2980₽

4. Бразилия Можиана
   - Цены: 250г — 820₽, 500г — 1550₽, 1кг — 2870₽

СТРОГИЕ ПРАВИЛА:
1. Используй ТОЛЬКО цены из этого списка. Не придумывай другие.
2. Если клиент спрашивает про сорт, которого НЕТ в списке (например, Робуста, Кения, Гватемала) — ответь: «Такого сорта у нас нет. У нас есть: Бленд Бразилия х Эфиопия, Эфиопия Сидамо, Колумбия Супремо, Бразилия Можиана.»
3. Если клиент спрашивает цену — назови ТОЧНУЮ цену из списка. Не округляй, не меняй.
4. Отвечай кратко (2-3 предложения).
5. Если клиент хочет заказать — спроси сорт, вес (250г/500г/1кг) и адрес.
6. Не давай общих советов — только по нашему каталогу.
"""

def save_request(user_id, text):
    """Сохраняет заказ в файл."""
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append({"user_id": user_id, "text": text})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ask_ai(user_text):
    """Отправляет запрос в нейросеть через ProxyAPI."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка AI: {e}")
        return "Извините, произошла ошибка. Попробуйте позже."

def get_main_keyboard():
    """Главное меню с кнопками."""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Каталог", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Прайс-лист", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Оформить заказ", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Доставка", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def get_catalog_keyboard():
    """Клавиатура с сортами кофе."""
    keyboard = VkKeyboard(one_time=False)
    for key, item in CATALOG.items():
        keyboard.add_button(item["name"][:40], color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def main():
    print("Бот запущен...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_text = event.obj.message.get("text", "").strip()
            user_id = event.obj.message.get("from_id")

            # === КОМАНДЫ ===
            if user_text.lower() in ["/start", "начать", "привет"]:
                vk.messages.send(
                    user_id=user_id,
                    message="Привет! Я бот магазина кофе в зернах «Кофе в удовольствие» ☕\nВыберите действие:",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Каталог
            if user_text.lower() == "каталог":
                text = "📋 Наш каталог:\n\n"
                for key, item in CATALOG.items():
                    text += f"{key}. {item['name']}\n"
                text += "\nНапишите номер сорта, чтобы узнать подробнее."
                vk.messages.send(
                    user_id=user_id,
                    message=text,
                    keyboard=get_catalog_keyboard(),
                    random_id=0
                )
                continue

            # Прайс-лист
            if user_text.lower() == "прайс-лист":
                text = "💰 Прайс-лист:\n\n"
                for key, item in CATALOG.items():
                    text += f"* {item['name']}\n{item['prices']}\n\n"
                vk.messages.send(
                    user_id=user_id,
                    message=text,
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Оформить заказ
            if user_text.lower() == "оформить заказ":
                vk.messages.send(
                    user_id=user_id,
                    message="Напишите: сорт, вес (250г/500г/1кг) и адрес доставки. Мы свяжемся для подтверждения.",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Доставка
            if user_text.lower() == "доставка":
                vk.messages.send(
                    user_id=user_id,
                    message="🚚 Доставка:\n- По России от 500₽\n- Самовывоз: ул. Кофейная, 1\n- Оплата: карта, СБП",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Назад
            if user_text.lower() == "назад":
                vk.messages.send(
                    user_id=user_id,
                    message="Главное меню:",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Выбор сорта по номеру
            if user_text in CATALOG:
                item = CATALOG[user_text]
                vk.messages.send(
                    user_id=user_id,
                    message=f"☕ {item['name']}\n\n{item['desc']}\n\n💰 Цены:\n{item['prices']}",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # Сохранение заказа
            if "заказ" in user_text.lower() or "оформить" in user_text.lower():
                save_request(user_id, user_text)
                vk.messages.send(
                    user_id=user_id,
                    message="Заказ принят! Мы свяжемся с вами для подтверждения.",
                    keyboard=get_main_keyboard(),
                    random_id=0
                )
                continue

            # === СВОБОДНЫЙ ВОПРОС → AI ===
            answer = ask_ai(user_text)
            vk.messages.send(
                user_id=user_id,
                message=answer,
                keyboard=get_main_keyboard(),
                random_id=0
            )

if __name__ == "__main__":
    main()
