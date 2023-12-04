import logging
from _lsprof import profiler_entry
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = Bot(token="6597297326:AAENgyOMwxllHeuLmG_SVMgoHZz5KuakF1k")
dp = Dispatcher(bot, storage=MemoryStorage())

class Stating(StatesGroup):
    instagram_link = State()
conn = sqlite3.connect('telegram_users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
''')
conn.commit()
conn.close()

@dp.message_handler(commands='start')
async def starter(message: types.Message):
    await message.answer("Assalomu alaykum, botga xush kelibsiz !\nBotdan foydalanish uchun instagram linkini yuboring !")
    await Stating.instagram_link.set()

@dp.message_handler(state=Stating.instagram_link, content_types=types.ContentType.TEXT)
async def videochi(message: types.Message):
    urls_user = message.text
    if urls_user.startswith('https://www.instagram.com/'):
        await message.answer('Video yuklanmoqda...')
        await message.answer_video(urls_user.replace("www.", "dd"),caption='Video yuklovchi bot\nAvtor: @rmkvlly')
        await message.answer('Video yuklandi')
    else:
        await message.answer("Instagram link kiriting !")

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def handle_new_member(message: types.Message):
    new_members = message.new_chat_members
    print(new_members)


    for user in new_members:
        user_id = user.id

        # Insert user ID into the SQLite database
        conn = sqlite3.connect('telegram_users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()


# if chat member is left the gruop delete user from database
@dp.message_handler(content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def handle_left_member(message: types.Message):
    left_member = message.left_chat_member
    print(left_member)

    user_id = left_member.id

    # Delete user ID from the SQLite database
    conn = sqlite3.connect('telegram_users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    #send message to group
    await message.answer(f"{left_member.full_name} guruxdan chiqdi")


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)



