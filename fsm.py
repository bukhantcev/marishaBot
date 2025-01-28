from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State



class NewItem(StatesGroup):
    messages = State()
    messages_user = State()
    messages_assistant = State()

