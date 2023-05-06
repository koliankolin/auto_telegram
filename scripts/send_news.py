import os
from telebot import TeleBot, formatting


TOKEN = os.environ.get('BOT_TOKEN')
channel_id = os.environ.get('CHANNEL_ID')
bot = TeleBot(
    token=TOKEN,
    parse_mode='html',
    disable_web_page_preview=True
)


if __name__ == '__main__':
    bot.send_message(
        chat_id=channel_id,
        text=f"{formatting.hbold('test message')}",
    )