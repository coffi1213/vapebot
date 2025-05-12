from aiogram import Dispatcher, types
from aiogram.type import InlineKeyboardMarkup, InlineKeyboardButton
from config import get_ref_link, MANAGER_CONTACT
from database import *
from utils.utils import format_cart_text, format_reviews_text
from states import ReviewState
from aiogram.dispatcher import FSMContext

# Команда /start
async def cmd_start(msg: types.Message):
    ref = msg.get_args()
    ref_id = int(ref) if ref and ref.isdigit() else None
    add_user(msg.from_user.id, ref_id)
    await msg.answer("Добро пожаловать! Используйте меню ниже.")

# Все товары
async def show_products(msg: types.Message):
    products = get_all_products()
    if not products:
        return await msg.answer("Товары временно отсутствуют.")
    for p in products:
        pid, name, desc, price, photo = p
        text = f"<b>{name}</b>\n{desc}\nЦена: {price}₽"
        kb.add(
            InlineKeyboardButton("Купить", url=MANAGER_CONTACT),
            InlineKeyboardButton("Добавить в корзину", callback_data=f"cart_{pid}"),
            InlineKeyboardButton("Оставить отзыв", callback_data=f"review_{pid}")
        )
        if photo:
            await msg.answer_photo(photo, caption=text, reply_markup=kb)
        else:
            await msg.answer(text, reply_markup=kb)

# Баллы + реферальная ссылка
async def show_points(msg: types.Message):
    points = get_user_points(msg.from_user.id)
    ref = get_ref_link(msg.from_user.id)
    await msg.answer(f"Ваши баллы: {points}\n\nВаша реферальная ссылка:\n{ref}")

# Корзина
async def show_cart(msg: types.Message):
    items = get_cart(msg.from_user.id)
    if not items:
        return await msg.answer("Ваша корзина пуста.")
    total, text = format_cart_text(items)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Оформить заказ", callback_data="checkout"))
    kb.add(InlineKeyboardButton("Очистить корзину", callback_data="clear_cart"))
    await msg.answer(text, reply_markup=kb)

# История заказов
async def show_history(msg: types.Message):
    order = get_user_orders(msg.from_user.id)
    if not orders:
        return await msg.answer("Вы еще ничего не покупали.")
    text = "\n".join([f"{name} - {date}" for name, date in orders])
    await msg.answer(f"<b>Ваша история покупок:</b>\n{text}")

# Callback: добавить в корзину
async def cb_add_cart(call: types.CallbackQuery):
    pid = int(call.data.split("_")[1])
    add_to_cart(call.from_user.id, pid)
    await call.answer("Товар добавлен в корзину!")

# Callback: оформить заказ
async def cb_checkout(call: types.CallbackQuery):
    items = get_cart(call.from_user.id)
    if not items:
        return await call.answer("Корзина пуста!")
    for item in items:
        record_order(call.from_user.id, item[0])
    clear_cart(call.from_user.id)
    await call.message.answer("Ваш заказ принят! Менеджер скоро свяжется.")

# Callback: очистить корзину
async def cb_review(call: types.CallbackQuery, state: FSMContext):
    pid = int(call.data.split("_")[1])
    await state.update_data(products_id=pid)
    await call.message.answer("Напишите свой отзыв:")
    await ReviewState.waiting_for_text.set()

# Сохранить отзыв 
async def save_review(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    add_review(msg.from_user.id, data["product_id"], msg.text)
    await msg.answer("Спасибо за ваш отзыв!")
    await state.finish()

# Регестрация хендлеров
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handlers(cmd_start, commands=["start"])
    dp.register_message_handlers(show_products, text="Все товары")
    dp.register_message_handlers(show_points, text="Баллы")
    dp.register_message_handlers(show_cart, text="Корзина")
    dp.register_message_handlers(show_history, text="История покупок")
    dp.register_callback_query_handler(cb_add_cart, lambda c: c.data.startswith("cart_"))
    dp.register_callback_query_handler(cb_checkout, lambda c: c.data == "checkout")
    dp.register_callback_query_handler(cb_clear_cart, lambda c: c.data == "clear_cart")
    dp.register_callback_query_handler(cb_review, lambda c: c.data.startswith("review_"), state="*")
    dp.register_message_handlers(save_review, state=ReviewState.waiting_for_text)