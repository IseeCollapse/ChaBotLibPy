import telebot
from spacy import load

# Токен бота
TOKEN = "7544768223:AAG_SeAcIrb5zuChFAqSQ25488DjFu1U06k"
# Имя модели Spacy для загрузки
MODEL_NAME = "ru_core_news_sm"

# Создание бота
bot = telebot.TeleBot(TOKEN)
# Загрузка модели Spacy
nlp = load(MODEL_NAME)

# Ответы на команды
COMMAND_RESPONSES = {
    "start": "Здравствуйте! Чем могу помочь?",
    "services": "Мы предоставляем IT-услуги, бухгалтерское сопровождение, промоушен и логистику.",
    "contacts": "Наши контактные данные: адрес в Краснодаре, телефон, email.",
    "schedule": "Мы работаем с понедельника по пятницу с 9:00 до 18:00.",
    "info": ("Бот может распознавать следующие слова:\n"
             "Услуги - выведет список актуальных предоставляемых услуг.\n"
             "Контакты - выведет список актуальных контактов.\n"
             "График - выведет актуальный график работы.")
}

# Лемматизированный словарь ключевых слов
KEYWORDS = {
        r"привет|здравствуйте|добрый день|добрый вечер": "start",
        r"услуга": "services",
        r"контакт": "contacts",
        r"время": "schedule"
}


@bot.message_handler(commands=['start', 'services', 'contacts', 'schedule', 'info'])
def handle_command(message):
    command = message.text.lstrip('/')
    response = COMMAND_RESPONSES.get(command, "Команда не распознана. Используйте /info для получения списка команд.")
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    doc = nlp(message.text.lower())
    response_sent = False

    for token in doc:
        lemma = token.lemma_
        if lemma in KEYWORDS:
            bot.send_message(message.chat.id, COMMAND_RESPONSES[KEYWORDS[lemma]])
            response_sent = True
            break

    if not response_sent:
        bot.send_message(message.chat.id, "Извините, я не понимаю вашего сообщения.")

bot.polling()



