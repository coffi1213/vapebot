from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def format_cart_text(items):
    total = sum(item[2] for item in items)
    text = "<b>Ваша корзина:</b>\n\n"
    for pid, name, price in items:
        text += f"- {name}: {price}₽\n"
    text += f"\n<b>Итого:</b> {total}₽"
    return total, text

def format_reviews_text(reviews):
    if not reviews:
        return "Отзывов пока нет."
    text = "<b>Отзывы:</b>\n"
    for comment, date in reviews:
        text += f"· {comment} ({date})\n"
    return text