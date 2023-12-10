import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from decouple import config
from aiogram.types import InputFile
from time import monotonic
import speedtest
import subprocess

from func import *
from utils import *
from store import *

def start_flask():
  clear()
  subprocess.Popen(["python3", "uptime.py"])


def update_bot():
  clear()
  subprocess.Popen(["python3", "update.py"])

logging.basicConfig(level=logging.INFO)

TOKEN = config('BOT_TOKEN', default='YOUR_BOT_TOKEN_HERE')
APIKEY = config('APIKEY', default='YOUR_APIKEY_HERE')
OWNER = config('OWNER', default='https://facebook.com/anbuinfosec')
ADMIN_ID = config('ADMIN_ID', default='5839119376')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    commands = [
        types.BotCommand(command='start', description='Start the bot'),
        types.BotCommand(command='help', description='Get help'),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello! Send me video url to download files.")

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    start_time = monotonic()
    processing_message = await message.reply("Pinging....")
    end_time = monotonic()
    ping = int((end_time - start_time) * 1000)
    s = speedtest.Speedtest()
    servers = s.get_servers()
    download_speed = s.download() / 1000000
    upload_speed = s.upload() / 1000000
    url = s.results.share()
    caption = (f'▣ Ping : {ping} ms\n▣ Download : {download_speed:.2f} Mbit/s\n▣ Upload : {upload_speed:.2f} Mbit/s')
    await processing_message.delete()
    await bot.send_photo(message.chat.id, photo=url, caption=caption)
    
@dp.message_handler(commands=['stats'])
async def stats(message: types.Message):
    await message.reply(get_system_info())

@dp.message_handler(commands=['cktmp'])
async def cktmp(message: types.Message):
    items = os.listdir('tmp')
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        processing_message = await message.reply("Checking tmp files!")
        if len(items) == 0:
            await processing_message.edit_text('Tmp folder is empty!')
        else:
            tmpFiles = "\n".join([f"{index}. {item}" for index, item in enumerate(items, start=1)])
            await processing_message.edit_text(tmpFiles)
    else:
        await message.answer("Hehe boi you are not bot admin.")

@dp.message_handler(commands=['clean'])
async def clean(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        processing_message = await message.reply("Please wait, deleting files!")
        tmp_folder = 'tmp'
        try:
            for item in os.listdir(tmp_folder):
                item_path = os.path.join(tmp_folder, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    os.rmdir(item_path)

            await processing_message.edit_text("Tmp folder cleaning successful.")
        except Exception as e:
            await processing_message.edit_text(f"An error occurred: {e}")
    else:
        await message.answer("Hehe boi you are not bot admin.")

@dp.message_handler()
async def echo(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    name = f"{first_name} {last_name}" if last_name else first_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id
    message_url = str(message.text)

    await check_tmp()
    downloader = check_downloader(message_url)
    if downloader:
        processing_message = await message.reply("Please wait, downloading file fro : {message_url}")
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        try:
            video_info = await get_video_download_info(message_url, downloader, APIKEY)
            if video_info["status"]:
                getShortUrl = urlShort(video_info['url'])
                if getShortUrl != False:
                    save_data(name, user_id, message_url, getShortUrl)
                    keyboard = types.InlineKeyboardMarkup()
                    end_button1 = types.InlineKeyboardButton(text="Author", url=OWNER)
                    end_button2 = types.InlineKeyboardButton(text="Repo", url="https://github.com/anbuinfosec/social-bot-v2")
                    end_button3 = types.InlineKeyboardButton(text="Download Link", url=getShortUrl)
                    keyboard.add(end_button1, end_button2, end_button3)
                else:
                    save_data(name, user_id, message_url, video_info['url'])
                    keyboard = types.InlineKeyboardMarkup()
                    end_button1 = types.InlineKeyboardButton(text="Author", url=OWNER)
                    end_button2 = types.InlineKeyboardButton(text="Repo", url="https://github.com/anbuinfosec/social-bot-v2")
                    keyboard.add(end_button1, end_button2, end_button3)
                file_path, size, file_type = await downloadFromUrl(video_info['url'])
                if file_path == False:
                    return await message.reply("Unable to download file!")
                await processing_message.edit_text("Video download successful. Please wait, uploading your file.")
                with open(file_path, 'rb') as video_file:
                    await bot.send_chat_action(chat_id, "upload_video")
                    if file_type == 'video':
                        await bot.send_video(chat_id=message.chat.id, video=InputFile(video_file))
                    elif file_type == 'photo':
                        await bot.send_photo(chat_id=message.chat.id, video=InputFile(video_file))
                    elif file_type == 'doc':
                        await bot.send_document(chat_id=message.chat.id, video=InputFile(video_file))
                    else:
                        await processing_message.delete()
                        os.remove(file_path)
                        return await message.reply("Invalid file type.", reply_markup=keyboard)
                    os.remove(file_path)
                    await message.reply("Thanks for using our bot.", reply_markup=keyboard)
            else:
                await processing_message.delete()
                os.remove(file_path)
                
                await message.reply('Download Failed!\nPress download button for download the video from url.', reply_markup=keyboard)
        except Exception as e:
            print (e)
            os.remove(file_path)
            await message.answer(f"Error: {str(e)}")
    else:
        print("[-] Unsupported URL")


if __name__ == '__main__':
    from aiogram import executor
    start_flask()
    update_bot ()
    clear ()
    executor.start_polling(dp, on_startup=on_startup)
