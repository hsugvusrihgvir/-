import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
from moviepy.editor import *
from random import randint, choice
from PIL import Image
from settings import TOKEN
import asyncio

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def random_cats():
    try:
        for i in range(5):
            response = requests.get("https://meow.senither.com/v1/random")
            if response:
                json_response = response.json()
                while json_response['data']['url'][-3:] != 'jpg':
                    response = requests.get("https://meow.senither.com/v1/random")
                    if response:
                        json_response = response.json()
                a = requests.get(json_response['data']['url'])
                with open("data\\" + str(i) + ".jpg", "wb") as f:
                    f.write(a.content)
    except:
        pass


def cut_images():
    for i in range(5):
        img = Image.open("data\\" + str(i) + ".jpg")
        w, h = img.size
        img = img.crop(((w - h // 16 * 9) // 2, 0, h // 16 * 9 + (w - h // 16 * 9) // 2, h))
        img = img.resize((1080, 1920))
        img.save('data\\' + str(i) + '.jpg')


def create_video():
    ic_1 = ImageClip('data\\0.jpg').set_duration(2)
    ic_2 = ImageClip('data\\1.jpg').set_duration(2)
    ic_3 = ImageClip('data\\2.jpg').set_duration(2)
    ic_4 = ImageClip('data\\3.jpg').set_duration(2)
    ic_5 = ImageClip('data\\4.jpg').set_duration(2)
    video = concatenate([ic_1, ic_2, ic_3, ic_4, ic_5], method="compose")
    a_cl = AudioFileClip("data\\sound\\" + str(randint(1, 8)) + ".mp3")

    video = video.set_audio(a_cl)
    video.write_videofile('res.mp4', fps=1)


def send_video(update, context):
    random_cats()
    cut_images()
    create_video()
    context.bot.send_video(chat_id=update.message.chat_id, video=open('res.mp4', 'rb'), supports_streaming=True)


def start(update):
    update.message.reply_text(
        "Привет! Хочешь видео с милыми котиками? Пиши /cats")


def help(update):
    update.message.reply_text(
        "Видео с котами - /cats\n"
        "Картинка - /cat")


def pphoto(update, context):
    response = requests.get("https://meow.senither.com/v1/random")
    json_response = response.json()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=choice(json_response['data']['url']))


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cat", pphoto))
    dp.add_handler(CommandHandler("cats", send_video))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
