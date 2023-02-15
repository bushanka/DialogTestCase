from aiogram import Bot, types, Dispatcher, executor
from src.secret.secret_data import BOT_TOKEN
from src.buttons.keyboard_buttons import main_keyboard
from src.parser.parse import parse_magnit

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Функция обрабатывает команду пользователя /start
    :param message:
    :return: None
    """
    await message.answer("Выберите город", reply_markup=main_keyboard)


@dp.message_handler()
async def handle_request(message: types.Message):
    """
    Обрабатывает сообщения пользователя, вызывает функцию парсинга данных с сайта
    :param message:
    :return: None
    """
    city = message.text
    if city == 'Москва' or city == 'Новосибирск':
        await message.answer('Загружаю...')
        file_name = await parse_magnit(city)
        await message.answer_document(open(file_name, 'rb'), reply_markup=main_keyboard)
    else:
        await message.answer("Используйте только кнопки", reply_markup=main_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
