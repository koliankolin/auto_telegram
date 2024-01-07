import os

from telebot import TeleBot, formatting


token = os.getenv("BOT_TOKEN")
bot = TeleBot(
    token=token,
    parse_mode="html",
    disable_web_page_preview=True
)
chat_id = os.getenv("CHAT_ID")

if __name__ == "__main__":
    # print(token)
    # print(chat_id)
    # bot.send_message(chat_id=chat_id, text=f"test from {formatting.hbold('python')}")
    bot.send_photo(chat_id=chat_id, photo=open("/home/ono/Downloads/Math1.png", "rb"), caption=f"{formatting.hbold('New logo')}")