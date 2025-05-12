from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from database import (
    get_all_users, set_user_points, get_user_points,
    get_total_orders, get_top_products, get_all_products
)
from states import AdminLoginState, EditPointsState
from config import ADMIN_PASSWORD
from keyboards.default import admin_menu

ADMINS = set()

# Авторизация
async def admin_login(msg: types.Message):
    await msg.answer("Введите пароль для входа в админ-панель:")
    await AdminLoginState.awaiting_password.set()

async def check_password(msg: types.Message, state: FSMContext):
    if msg.text == ADMIN_PASSWORD:
        ADMINS.add(msg.from_user.id)
        await msg.answer("Доступ разрешен", reply_markup=admin_menu())
        await state.finish()
    else:
        await msg.answer("Неверный пароль")

# Просмотр всех пользователей
async def view_users(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("Нет доступа")
    users = get_all_users()
    text = "\n".join([f"ID: {uid} - {points} баллов" for uid, points in users])
    await msg.answer(text or "Пользователей нет")

# Изменение баллов пользователя (через FSM)
async def edit_points_start(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("Нет доступа")
    await msg.answer("Введите ID пользователя:")
    await EditPointsState.awaiting_user_id.set()

async def edit_points_id(msg: types.Message, state: FSMContext):
    await state.update_data(user_id=msg.text)
    await msg.answer("Введите новое количество баллов:")
    await EditPointsState.awaiting_amount.set()

async def edit_points_amount(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        uid = int(data["user_id"])
        amount = int(msg.text)
        set_user_points(uid, amount)
        await msg.answer(f"Баллы пользователя {uid} обновлены до {amount}")
    except:
        await msg.answer("Ошибка ввода")
    await state.finish()

# Статистика
async def show_stats(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("Нет доступа")

    users = get_all_users()
    products = get_all_products()
    orders = get_total_orders()
    top = get_top_products()

    text = (
        f"<b>Статистика бота:</b>\n"
        f"Пользователей: {len(users)}\n"
        f"Товаров: {len(products)}\n" 
        f"Всего заказов: {orders}\n\n" 
        f"<b>Топ товары:</b>\n"
    )

    for pid, total in top:
        name = next((p[1] for p in products if p[0] == pid), "Неизвестно")
        text += f"- {name}: {total} заказов\n"

    await msg.answer(text)

# Регестрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handlers(admin_login, commands=["admins"], state="*")
    dp.register_message_handlers(check_password, state=AdminLoginState.awaiting_password)
    dp.register_message_handlers(view_users, text="Пользователи")
    dp.register_message_handlers(edit_points_start, text="Изменить баллы")
    dp.register_message_handlers(edit_points_id, state=EditPointsState.awaiting_user_id)
    dp.register_message_handlers(edit_points_amount, state=EditPointsState.awaiting_amount)
    dp.register_message_handlers(show_stats, text="Статистика")