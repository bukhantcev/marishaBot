import asyncio
import os

import openai
from aiogram.dispatcher.filters import Text
from openai import OpenAI
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from fsm import NewItem
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import roles






TIMEOUT = 300
tasks = {}
memory = MemoryStorage()



OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
def get_ai_response(user_input, role:str, messages:list):

    try:
        # Отправляем запрос к OpenAI API
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Используемая модель
        messages=messages,
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
dp = Dispatcher(bot, storage=memory)

# Обработчик текстовых сообщений (Эхо-бот)
@dp.message_handler(Text(equals="давай поговорим", ignore_case=True))
async def echo_message(message: Message, state:FSMContext):

    await NewItem.messages.set()  # Устанавливаем состояние

    if message.chat.id == 404354012 or message.chat.id == 857601623:
        role = roles.role_m if message.chat.id == 857601623 else roles.role_s
        messages = [{"role": "system", "content": role},
                    {"role": "user", "content":message.text},
                    ]
        if message.chat.id == 857601623:
            await bot.send_message(chat_id=404354012, text=message.text)
            answer = get_ai_response(message.text, role=role, messages=messages)
            await bot.send_message(chat_id=404354012, text=answer)
        if message.chat.id == 404354012:
            answer = get_ai_response(message.text, role=role, messages=messages)

        await message.answer(answer)
        messages.append({"role": "assistant", "content":answer})
        task = asyncio.create_task(auto_finish_fsm(message.chat.id, state, TIMEOUT))
        tasks[message.chat.id] = task
        print('dialog')

    else:
        await message.answer("Уходи, я не хочу с тобой разговаривать!")


@dp.message_handler(state=NewItem.messages)
async def echo_message(message: Message, state:FSMContext):


    if message.chat.id == 404354012 or message.chat.id == 857601623:
        # Получаем задачу из словаря и отменяем её
        task = tasks.pop(message.chat.id, None)
        if task:
            task.cancel()  # Отмена таймера
        role = roles.role_m if message.chat.id == 857601623 else roles.role_s
        data = await state.get_data()

        if 'messages' not in data:
            messages = [{"role": "system", "content": role},
                        {"role": "user", "content":message.text},
                        ]
        else:
            messages = data['messages']
            messages.append({"role": "user", "content": message.text})


        if message.chat.id == 857601623:
            await bot.send_message(chat_id=404354012, text=message.text)
            answer = get_ai_response(message.text, role=role, messages=messages)
            await bot.send_message(chat_id=404354012, text=answer)
        if message.chat.id == 404354012:
            answer = get_ai_response(message.text, role=role, messages=messages)

        await message.answer(answer)
        messages.append({"role": "assistant", "content": answer})

        await state.update_data(messages=messages)
        task = asyncio.create_task(auto_finish_fsm(message.chat.id, state, TIMEOUT))
        tasks[message.chat.id] = task
        print('dialog')
        if str(message.text).lower() == 'пока':
            await state.finish()
            print('off dialog')


    else:
        await message.answer("Уходи, я не хочу с тобой разговаривать!")




@dp.message_handler()
async def echo_message(message: Message):


    if message.chat.id == 404354012 or message.chat.id == 857601623:
        role = roles.role_m if message.chat.id == 857601623 else roles.role_s
        messages = [{"role": "system", "content": role},
                    {"role": "user", "content": message.text},
                    ]
        if message.chat.id == 857601623:
            await bot.send_message(chat_id=404354012, text=message.text)
            answer = get_ai_response(message.text, role=role, messages=messages)
            await bot.send_message(chat_id=404354012, text=answer)
        if message.chat.id == 404354012:
            answer = get_ai_response(message.text, role=role, messages=messages)

        await message.answer(answer)

    else:
        await message.answer("Уходи, я не хочу с тобой разговаривать!")


async def auto_finish_fsm(chat_id: int, state: FSMContext, timeout: int):
    try:
        await asyncio.sleep(timeout)  # Ждём тайм-аут
        current_state = await state.get_state()
        if current_state:  # Если пользователь всё ещё в состоянии
            await state.finish()  # Завершаем FSM
            await bot.send_message(chat_id, "Ну вот и поговорили...")
    except asyncio.CancelledError:
        # Если таймер был отменён
        print(f"Таймер для пользователя {chat_id} был отменён.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # Запуск бота
