import os
from telebot import TeleBot
import time
from random import choice
import logging

from news_sources import WorldNYTimesNewsSource, USANYTimesNewsSource

logging.basicConfig(level=logging.INFO)

bot = TeleBot(
    token=os.environ.get("BOT_TOKEN"),
    parse_mode='html',
    disable_web_page_preview=True
)
chat_id = os.environ.get("CHANNEL_ID")
sources = [
    WorldNYTimesNewsSource(),
    USANYTimesNewsSource()
]
news_to_post = int(os.environ.get("NEWS_TO_POST") or 3)


if __name__ == '__main__':
    logging.info(f"News to post: {news_to_post}")

    while news_to_post:
        source = choice(sources)

        news = source.get_one_news()
        photo = source.create_mem_from_photo(news=news)
        caption = source.construct_caption(news=news)

        bot.send_photo(
            chat_id=chat_id,
            photo=open(photo, 'rb'),
            caption=caption
        )
        logging.info(f"News {news.title} was sent")
        photo.unlink()
        time.sleep(5)
        news_to_post -= 1
