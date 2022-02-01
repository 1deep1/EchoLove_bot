from random import choice
import telebot
from telebot import types
import urllib
import os

import love
from auth import token

import time
from datetime import datetime


def mainImg():
    url = "https://sun9-30.userapi.com/impg/MS1lPdhq7C2vZWLZ54n9EMZ27mzP0WwrmiEJ8Q/ckCjgK7I3yM.jpg?size=1041x1080&quality=96&sign=31807878798fb300952299e9a8a816fe&type=album"
    f = open('out.jpg','wb')
    f.write(urllib.request.urlopen(url).read())
    f.close()

def echolove_bot(token):
    bot = telebot.TeleBot(token)

    # /start
    @bot.message_handler(commands=["start"])
    def start_message(message):
        chat = message.chat.id
        bot.send_message(message.chat.id, "Привет, моя любимая кошечка 💕\nТеперь я всегда буду с тобой!!!\n\nЯ могу говорить как сильно я тебя люблю, отправлять милые картинки и иногда просто так напоминать о себе\n\n(v0.0.2) Бот будет получать новые функции и обновляться во имя нашей любви!")
        # Отправить фото
        mainImg()
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        
        # Меню
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1=types.KeyboardButton("Как сильно ты меня любишь?")
        item2=types.KeyboardButton("Мяшную пикчу, пожалуйста")
        item3=types.KeyboardButton("МЕГА любовь")

        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id,'Тыкни для любви:',reply_markup=markup)
    
    # Обработчик текста
    @bot.message_handler(content_types=['text'])
    def message_reply(message):
        if message.chat.type == 'private':
            if message.text=="Как сильно ты меня любишь?":
                bot.send_message(message.chat.id,love.loveText())
            elif message.text == "Мяшную пикчу, пожалуйста":
                love.lovePhoto(message, bot)
            elif message.text == "МЕГА любовь":
                sent = bot.send_message(message.chat.id, 'Введи силу любви (от 1 до 4000):')
                bot.register_next_step_handler(sent, mega)
            elif message.text == 'любовь':
                sent = bot.send_message(message.chat.id, 'Введи фразу:')
                bot.register_next_step_handler(sent, save_text)
            elif message.text == "chat":
                bot.send_message(message.chat.id, message.chat.id)
    
    def save_text(message):
        file = "/home/admin/echoBot/loveText.txt"
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n' + message.text)
        bot.reply_to(message, "Пожалуй, я сохраню это во имя нашей любви")

    def mega(message):
        err = "Прости, видимо ты ввела не то значение(("
        out = ""
        if message.text.isdigit():
            if int(message.text) > 0 and int(message.text) < 4001:
                file = "/home/admin/echoBot/loveText.txt"
                with open(file, encoding='utf-8') as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                text = choice(content)

                
                for x in range(int(message.text)):
                    out += text + "\n"
                if len(out) > 4095:
                    for x in range(0, len(out), 4095):
                        bot.reply_to(message, text=out[x:x+4095])
                else:
                    bot.reply_to(message, text=out)
            else:
                bot.reply_to(message, err)
        else:
            bot.reply_to(message, err)
    
    # Обработчик файлов
    @bot.message_handler(content_types=['document'])
    def handle_docs_photo(message):
        try:
            files = os.listdir('/home/admin/echoBot/pic/')
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = '/home/admin/echoBot/pic/out' + str(len(files)) + '.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, "Пожалуй, я сохраню это во имя нашей любви")
        except Exception as e:
            bot.reply_to(message, e)
    
    # Обработчик фото
    @bot.message_handler(content_types=['photo'])
    def handle_docs_photo(message):
        try:
            files = os.listdir('/home/admin/echoBot/pic/')
            file_info = bot.get_file(message.photo[0].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = '/home/admin/echoBot/pic/out' + str(len(files)) + '.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, "Пожалуй, я сохраню это во имя нашей любви")
        except Exception as e:
            bot.reply_to(message, e)

    bot.infinity_polling()

if __name__ == '__main__':
    echolove_bot(token)
