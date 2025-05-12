from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

# Главное меню для пользователя
def user_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("Все товары"),
        KeyboardButton("Корзина")
    ).add(
        KeyboardButton("Баллы"),
        KeyboardButton("История покупок")
    )
    return kb

# Админ-панель после авторизации
def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("Пользователи"),
        KeyboardButton("Изменить баллы")
    ).add(
        KeyboardButton("Статистика")
    )
    return kb