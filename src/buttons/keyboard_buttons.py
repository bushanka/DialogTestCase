from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

button_moscow = KeyboardButton('Москва')
button_novosib = KeyboardButton('Новосибирск')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_moscow, button_novosib)
