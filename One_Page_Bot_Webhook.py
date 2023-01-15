import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'your bot token should be here'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

TELEGRAM_SUPPORT_CHAT_ID = "id of support chat should be here"
URL_APP = "server url should be here"

async def on_startup(dp):
    await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, 'Я включился :)')
    await bot.set_webhook(URL_APP)

async def on_shutdown(dp):
    await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, 'Я выключился :(')
    await bot.delete_webhook()

# handlers

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.reply("Hello!\nЗYou can ask your questions here :)\n\nIf you're sending photos or files please send rhem one by one")

@dp.message_handler(commands=['help'])
async def send_no_help(message: types.Message):
   await message.reply("Hello!\nЗYou can ask your questions here :)\n\nIf you're sending photos or files please send rhem one by one")


# from support to client

#bot will only send message if it starts with "Client ID: #client{id}"
#All other messages in chat would not be sent

@dp.message_handler(chat_type=[types.ChatType.GROUP])
async def support_answer(message: types.Message):
    if message.chat.id == int(TELEGRAM_SUPPORT_CHAT_ID):
        if 'Client' in message.text.split(' ') and 'ID:' in message.text.split(' '):
            Not_Yet_Client_ID = message.text.split(' ')[2]
            Client_ID = Not_Yet_Client_ID.split('/n')[0][7:]
            await message.reply("Sent!")
            text_clear = ''
            for i in message.text.split('\n')[1:]:
                text_clear += i + '\n'   #making the message without client id
            text_clear = text_clear[:-1]
            await bot.send_message(Client_ID, text=text_clear)

@dp.message_handler(chat_type=[types.ChatType.GROUP], content_types='photo')
async def support_answer(message: types.Message):
    if message.chat.id == int(TELEGRAM_SUPPORT_CHAT_ID):
        if 'Client' in message.caption.split(' ') and 'ID:' in message.caption.split(' '):
            Not_Yet_Client_ID = message.caption.split(' ')[2]
            Client_ID = Not_Yet_Client_ID.split('/n')[0][7:]
            await message.reply("Sent!")
            text_clear = ''
            for i in message.caption.split('\n')[1:]:
                text_clear += i + '\n'
            text_clear = text_clear[:-1]
            await bot.send_photo(Client_ID, message.photo[-1].file_id, text_clear)

@dp.message_handler(chat_type=[types.ChatType.GROUP], content_types='document')
async def support_answer(message: types.Message):
    if message.chat.id == int(TELEGRAM_SUPPORT_CHAT_ID):
        if 'Client' in message.caption.split(' ') and 'ID:' in message.caption.split(' '):
            Not_Yet_Client_ID = message.caption.split(' ')[2]
            Client_ID = Not_Yet_Client_ID.split('/n')[0][7:]
            await message.reply("Отправлено!")
            text_clear = ''
            for i in message.caption.split('\n')[1:]:
                text_clear += i + '\n'
            text_clear = text_clear[:-1]
            await bot.send_document(Client_ID, message.document.file_id)
            await bot.send_message(Client_ID, text=text_clear)

# from client to support

@dp.message_handler()
async def client_message(message: types.Message):
    if message.chat.id != int(TELEGRAM_SUPPORT_CHAT_ID):
        await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, f"User: {message.from_user.username}\nId: #client{message.from_user.id}\nMessage: " + message.text)

@dp.message_handler(content_types='photo')
async def client_message(message: types.Message):
    if message.chat.id != int(TELEGRAM_SUPPORT_CHAT_ID):
        await bot.send_photo(TELEGRAM_SUPPORT_CHAT_ID, message.photo[-1].file_id, f"User: {message.from_user.username}\nId: #client{message.from_user.id}\nCaption: " + str(message.caption))

@dp.message_handler(content_types='document')
async def client_message(message: types.Message):
    if message.chat.id != int(TELEGRAM_SUPPORT_CHAT_ID):
        await bot.send_document(TELEGRAM_SUPPORT_CHAT_ID, message.document.file_id)
        await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, f"User: {message.from_user.username}\nId: #client{message.from_user.id}\nCaption: " + str(message.caption))

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get('PORT', 5000)))
