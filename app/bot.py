import datetime

import telebot
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlretrieve
import os
import shutil
import random
from telebot import apihelper
from PIL import Image
import requests

from config import token

session = requests.Session()


def download_picture(text):
    os.system('python downloader.py -s {} -o pics --limit 6'.format(text.replace(' ', '+')))

def put_into_pants(text):
    dir = "pics"
    try:
        download_picture(text)
        text = text.upper()
        print(text)
        back = Image.open('jeans.png').resize((512, 512))
        img_name = random.choice([x for x in os.listdir(dir) if os.path.isfile(os.path.join(dir, x))])
        img_name = os.path.join(dir, img_name)
        front = Image.open(img_name, 'r').resize((160, 160))
        back.paste(front, (175, 5))
        fnt = ImageFont.truetype('impact.ttf', 30)
        d = ImageDraw.Draw(back)
        d.text((100, 420), "    {}\n    У ТЕБЯ В ШТАНАХ".format(text.upper()), font=fnt, fill=(0, 0, 0))
        back.save('result.png', format='png')
    except:
        raise
    finally:
        shutil.rmtree(dir)



def break_if_too_long(string, widthsize=38):
    if len(string) > widthsize * 2:
        string = string[:38] + '\n         ' + string[38:76] + '\n         ' + string[76:]
        return string
    if len(string) > widthsize:
        string = string[:38] + '\n         ' + string[38:]
    return string


def cut_into_sticker(path):
    basewidth = 512
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    if img.size[1] > 512:
        img = img.crop((0, 0, 512, 512))
    print(img.size)
    img.save(path)


bot = telebot.TeleBot(token)
time_limits = dict()
cooldown_seconds = 5

@bot.message_handler(content_types=["text", "photo"])
def handle(message):
    user = message.chat.id
    now = datetime.datetime.now()
    proper_time = now - datetime.timedelta(seconds=cooldown_seconds)

    if time_limits.get(user, proper_time) > proper_time:
        time_limits[user] = now
        bot.send_message(chat_id=message.chat.id, text='Ты пишешь слишком часто, подожди')
        return

    time_limits[user] = now

    try:
        print('-' * 80)
        text = message.text
        put_into_pants(text)
        bot.send_photo(chat_id=message.chat.id, photo=open('result.png', 'rb'))
    except:
        bot.send_message(chat_id=message.chat.id, text='Я не смогла найти хорошую картинку для этого')


if __name__ == '__main__':
    print("Start")
    bot.polling(none_stop=True, timeout=60)
