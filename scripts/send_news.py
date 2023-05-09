import os
from telebot import TeleBot, formatting


bot = TeleBot(
    token=os.environ.get("BOT_TOKEN"),
    parse_mode='html',
    disable_web_page_preview=True
)
chat_id = os.environ.get("CHANNEL_ID")


if __name__ == '__main__':
    bot.send_photo(
        chat_id=chat_id,
        photo=open('/Users/stanislav.gorchakov/Desktop/cat.jpeg', 'rb'),
        caption=f"{formatting.hbold('Awesome cat')}"
    )
