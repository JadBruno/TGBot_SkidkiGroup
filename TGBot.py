from cgitb import text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_reader import config
import pymysql
import pymysql.cursors

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot)

#Подключение к базе данных MySQL
def connect_bd():
    db_host = '23.105.226.124'
    db_port = 3306
    db_user = 'tg_bot_test_user'
    db_password = 'bJ3mI2zA2b'
    db_name = 'tg_bot_db'
    db_charset = 'utf8'
    connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                    charset=db_charset, cursorclass=pymysql.cursors.DictCursor)
    return connection

#Скачивание каталога из БД
def gain_categories():
    connection = connect_bd()
    with connection.cursor() as cursor:
            sql_records = "SELECT `wb_category_name` FROM `tg_wb_categories`"
            cursor.execute(sql_records)
            return cursor.fetchall()
    
#Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [[
           types.KeyboardButton(text="📔 Каталог"),
           types.KeyboardButton(text="❓ Как получить скидку"),
        ],]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Добрый день!\nВ этом канале мы расскажем Вам как приобрести наши товар на Wildberries со скидкой до 100%\nПосмотрите раздел "Как получить скидку?" или сразу переходите в "Каталог" к выбору товаров.', reply_markup=keyboard)        
    
#Обработка любого сообщения пользователя
@dp.message_handler()
async def reply(message: types.Message):
    global connection
    #Обработка нажатия кнопки Каталог
    if message.text == "📔 Каталог":
        catalog_categories = gain_categories()
        for el in catalog_categories:
            await message.answer(el["wb_category_name"])   
    
    #Обработка нажатия кнопки Как получить скидку
    if message.text == "❓ Как получить скидку":
        await message.answer("Выберите товар и нажмите на кнопку под ним, кэшбэк зафиксируется в нашей системе\nПерейдите по ссылке на Wildberies и купите его")  

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)        