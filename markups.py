from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
    )
from database.models import StatusChoices

def help_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    btns = [
        InlineKeyboardButton("Админ панель", callback_data="admin"),
        InlineKeyboardButton("Меню", callback_data="menu"),
        InlineKeyboardButton("Туториал", url="https://youtu.be/dQw4w9WgXcQ")
    ]
    markup.add(*btns)
    return markup


def orders_markup(order):
    markup = InlineKeyboardMarkup()
    btns = [
        InlineKeyboardButton("Редактировать", callback_data=f"edit_{order.id}"),
    ]
    if order.status == StatusChoices.ordering:
        btns.append(InlineKeyboardButton("Завершить", callback_data=f"status_complete_{order.id}"))
    elif order.status == StatusChoices.active:
        btns.append(InlineKeyboardButton("Отменить", callback_data=f"status_reject_{order.id}"))
        btns.append(InlineKeyboardButton("Закрыть прием заказов", callback_data=f"status_close_{order.id}"))
    markup.row_width = 2
    markup.add(*btns)
    return markup


def edit_field_buttons(order_id):
    markup = InlineKeyboardMarkup(row_width=2)
    btns = [
        InlineKeyboardButton("Cсылка на заведение", callback_data=f"field_cafeurl_{order_id}"),
        InlineKeyboardButton("Комментарий",  callback_data=f"field_notice_{order_id}"),
        InlineKeyboardButton("Общая сумма",  callback_data=f"field_totalsum_{order_id}"),
    ]
    markup.add(*btns)
    return markup