from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.manager import order_manager
from aiogram import types
from aiogram import Dispatcher

from  markups import orders_markup, edit_field_buttons
# from bot import dp
# dp = Dispatcher(bot)

class FSMadmin(StatesGroup):
    url = State()
    notice = State()

class OrderEditState(StatesGroup):
    value = State()
    field = State()
    order_id = State()


# @dp.message_handler(commands="download", storage=None)
async def fsm_start(message: types.Message):
    if await order_manager.check_order():
        return await message.answer("У вас уже есть активный заказ! /orders")
    await FSMadmin.url.set()
    await message.reply("Отправьте ссылку на заведение , из которого будете заказывать")


# @dp.message_handler(content_types=["photo"], state=FSMadmin.photo)
async def load_url(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["url"] = message.text 
    await FSMadmin.next()
    await message.reply("Дайте коментарий к заказу и укажите способ оплаты ")



# @dp.message_handler(state=FSMadmin.name)
async def load_notice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["notice"] = message.text
        if await order_manager.check_order():
            await message.answer("Существует уже активный, закройте его, чтобы начать новый! \orders")
            await state.finish()
            return
        await order_manager.create_new_order(data)
    await state.finish()
    await message.reply("ваши данные успешно сохранены")



# @dp.message_handler(state=FSMadmin.description)
# async def load_description(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["description"] = message.text
#     await FSMadmin.next()
#     await message.reply("Дайте цену блюду")


# # @dp.message_handler(state=FSMadmin.price)
# async def load_price(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["price"] = message.text
        
#     async with state.proxy() as data:
#         await message.answer(text=str(data))
#         await message.answer(text="Блюдо дописано")    


async def get_orders(message: types.Message):
    orders = await order_manager.get_orders()
    for order in orders:
        markup = orders_markup(order)
        text = f"Заказ из сайта: {order.cafe_url}"
        text += f"\nСтатус заказа: {order.status}"
        text += f"\nКомментарий: `{order.notice}`"
        text += f"\n Сумма: {order.total_sum}"
        await message.answer(text, reply_markup=markup)


async def change_order_status(callback:types.CallbackQuery):
    data = callback.data
    message = callback.message
    data = data.split("_")
    await order_manager.change_order_status(data[1], data[2])
    await message.edit_text(f"Данные заказа обновлены!")

async def edit_cafe_order(callback: types.CallbackQuery):
    message = callback.message
    data = callback.data
    data = data.split("_")
    await OrderEditState.order_id.set()
    await OrderEditState.field.set()
    markup = edit_field_buttons(data[1])
    await message.edit_text("Выберите поля для редактирования: ", reply_markup=markup)


async def edit_order_buttons(callback: types.CallbackQuery, state: FSMContext): 
    message = callback.message
    data = callback.data
    data = data.split("_")
    text = "Отправьте новое значения для поля: "
    async with state.proxy() as state_data:
        state_data["order_id"] = data[2]
        if data[1] == "cafeurl":
            state_data["field"] = "cafe_url"
            text += "Ссылку на заведение"
        elif data[1] == "notice":
            state_data["field"] = "notice"
            text += "Комментарий к заказу"
        elif data[1] == "totalsum":
            state_data["field"] = "total_sum"
            text += "Общая сумма"
    await OrderEditState.value.set()        
    await message.edit_text(text)


async def order_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["value"] = message.text
        print(data)
        await message.answer("Новые данные сохранены в базу")
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands="new_order", storage=None)
    dp.register_message_handler(load_url , state=FSMadmin.url)
    dp.register_message_handler(load_notice, state=FSMadmin.notice)
    dp.register_message_handler(get_orders, commands=["orders"])

    # callback registers
    dp.register_callback_query_handler(
        change_order_status, 
        lambda c: str(c.data).startswith("status") 
        )
    
    dp.register_callback_query_handler(
        edit_cafe_order,
        lambda c: str(c.data).startswith("edit_")
    )

    dp.register_callback_query_handler(
        edit_order_buttons,
        lambda c: str(c.data).startswith("field_")
    )

    dp.register_message_handler(order_edit, state=OrderEditState.value)

    # dp.register_message_handler(load_descrip.tion, state=FSMadmin.description)
    # dp.register_message_handler(load_pric.e, state=FSMadmin.price)