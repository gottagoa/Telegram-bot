from aiogram import types
from markups import help_markup

from database.manager import user_manager


async def welcome_message(message: types.Message):
    user_data = {
        "username": message.from_user.username,
        "tg_id": message.from_user.id,
        "first_name": message.from_user.first_name,
    }
    await user_manager.register_user(user_data)
    text = f"Hello, {user_data['username']}. Send /help to see what I can do."
    await message.reply(text=text)



async def help_message(message: types.Message):
    markup = help_markup()
    await message.reply(text="Выберите вариант", reply_markup=markup)



def register_handler_client(dp):
    dp.register_message_handler(welcome_message, commands=["start"])
    dp.register_message_handler(help_message, commands=["help"])