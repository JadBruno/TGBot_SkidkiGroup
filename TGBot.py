from aiogram import Bot, Dispatcher, executor, types
import pymysql
import pymysql.cursors


API_TOKEN = '5641081713:AAE2--GwtG1P8t5LHxEYKqY5dXT-mMzWJRk'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db_host = '23.105.226.124'
db_port = 3306
db_user = 'tg_bot_test_user'
db_password = 'bJ3mI2zA2b'
db_name = 'tg_bot_db'
db_charset = 'utf8'
connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                 charset=db_charset, cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
        sql_records = "SELECT `product_category_name` FROM `product_category`"
        cursor.execute(sql_records)
        result = cursor.fetchall()
        
# from aiogram import types
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["С пюрешкой", "Без пюрешки"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)
        
@dp.message_handler(commands=['catalog'])
async def send_welcome(message: types.Message):
   for el in result:
      await message.answer(el["product_category_name"])

# @dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
# async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
#     await message.answer(message.text)
   

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)