from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def product_inline_keyboard(product_id: int, manager_link: str):
    kb.add(
        InlineKeyboardButton("Купить", url=manager_link),
        InlineKeyboardButton("Добавить в корзину", callback_data=f"cart_{product_id}"),
        InlineKeyboardButton("Оставить отзыв",callback_data=f"review_{product_id}")
    )
    return kb

def admin_product_controls(product_id: int):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Редактировать", callback_data=f"edit_{product_id}"),
        InlineKeyboardButton("Удалить", callback_data=f"delete_{product_id}")
    )
    return kb