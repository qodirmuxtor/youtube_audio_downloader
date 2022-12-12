import os
from pytube import YouTube
import telebot
from my_token import token


"""Youtube dan vediolarning audiosini yuklash uchun funksiya"""
def downloader(url):
    """yuklovchi funksiya"""
    
    """obyekt yaratib olamiz"""
    yt = YouTube(url) 

    """sozlamalarni to'g'irlab olamiz"""
    stream = yt.streams.filter(only_audio=True).first()

    """faylni yuklaymiz"""
    stream.download()
    title = yt.title
    
    """mp4 faylni mp3 faylga aylantirib olamiz"""
    my_file = f"{title}.mp4"
    base = os.path.splitext(my_file)[0]
    os.rename(my_file, base + '.mp3')
    
    return title


"""botni ishga tushurish uchun funksiya"""
def start_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Send me YouTube vedio link..!")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        text = message.text
        chat_id = message.chat.id
        print(text)

        #agar matn link bo'lsa quyidagi shart bajariladi
        if (text.startswith("https://www.youtube.com/watch?v=") and len(text) == 43) or (text.startswith("https://youtu.be/") and len(text) == 28):
            bot.reply_to(message, "Please Wait..!")
            
            #yuklovchi funksiyamizni ishga tushiramiz
            title = downloader(text)
            
            #yuklangan audioni junatamiz
            try:
                audio = open(f"{title}.mp3", 'rb')
                bot.send_audio(chat_id, audio)
                bot.send_audio(chat_id, "FILEID")
            except:
                pass
            #yuborilganda keyin audioni o'chirib tashlaymiz
    
        #agar matn link bo'lmasa quyidagi shart bajariladi
        else:
            bot.reply_to(message, "Something Wrong, Please try again..!")
               
            

    bot.infinity_polling()
    
    
    
"""botni ishga tushiramiz"""
start_bot(token)
