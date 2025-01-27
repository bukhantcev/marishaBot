import os

import openai
from openai import OpenAI
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor


# Укажите ваш API-ключ OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
def get_ai_response(user_input, role:str):
    try:
        # Отправляем запрос к OpenAI API
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Используемая модель
        messages=[
            {"role": "system", "content": role},  # Системное сообщение для настройки поведения
            {"role": "user", "content": user_input}  # Сообщение от пользователя
        ],
        max_tokens=1000,  # Максимальное количество токенов в ответе
        temperature=0.7)
        # Получаем текст ответа
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        return f"Ошибка: {e}"



# Установите ваш API-ключ Telegram Bot
API_TOKEN = os.getenv('TOKEN')


# Включаем логирование для отладки
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик текстовых сообщений (Эхо-бот)
@dp.message_handler()
async def echo_message(message: Message):

    if message.chat.id == 404354012 or message.chat.id == 857601623:
        if message.chat.id == 857601623:
            role = ("Ты будешь меня хвалить. Обращайся ко мне как к девушке в женском роде. Называй меня Мариша, Маришенька, "
                    "Мариночка, Солнышко, Солнце, Маришечка")
            await bot.send_message(chat_id=404354012, text=message.text)
            answer = get_ai_response(message.text, role=role)
            await bot.send_message(chat_id=404354012, text=answer)
        if message.chat.id == 404354012:
            role = ("Ты программист и умный помощник")
            answer = get_ai_response(message.text, role=role)
        await message.answer(answer)
    else:
        await message.answer("Уходи, я не хочу с тобой разговаривать!")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # Запуск бота
