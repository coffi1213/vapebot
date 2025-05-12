from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminState(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()

class ReviewState(StatesGroup):
    waiting_for_text = State()

class AdminLoginState(StatesGroup):
    awaiting_password = State()

class EditPointsState(StatesGroup):
    awaiting_user_id = State()
    awaiting_amount = State()