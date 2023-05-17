import os
import time
import requests

from telebot import TeleBot

from news_sources.nytimes_news_source import NYTimesNewsSource


bot = TeleBot(
    token=os.environ.get("BOT_TOKEN"),
    parse_mode='html',
    disable_web_page_preview=True
)
chat_id = os.environ.get("CHANNEL_ID")
source = NYTimesNewsSource()


if __name__ == '__main__':
    news_to_post = source.get_news()
    for news in news_to_post:
        photo = requests.get(news.img_url).content
        caption = source.construct_message(news=news)

        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption
        )
        print(f"News: {caption} was sent")
        time.sleep(5)
