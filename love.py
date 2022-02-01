# coding: utf-8
import codecs
import os
import random
from random import choice


def loveText():
    file = "/home/admin/echoBot/loveText.txt"
    with open(file, encoding='utf-8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    out = choice(content)
    return out

def lovePhoto(message, bot):
    files = os.listdir('/home/admin/echoBot/pic/')
    link = "/home/admin/echoBot/pic/out" + str(random.randrange(0, len(files), 1)) + ".jpg"
    img = open(link, 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()