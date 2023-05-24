import os
from telebot import TeleBot
import time
from random import choice
import logging

from news_sources import WorldNYTimesNewsSource, USANYTimesNewsSource
from utils.alerting import handle_exception


logging.basicConfig(level=logging.INFO)

bot = TeleBot(
    token=os.environ.get("BOT_TOKEN"),
    parse_mode='html',
    disable_web_page_preview=True
)
chat_id = os.environ.get("CHANNEL_ID")
news_to_post = int(os.environ.get("NEWS_TO_POST") or 3)
sources = [
    WorldNYTimesNewsSource(),
    USANYTimesNewsSource()
]


if __name__ == '__main__':
    logging.info(f"News to post: {news_to_post}")

    try:
        while news_to_post:
            source = choice(sources)

            news = source.get_one_news()
            if not news:
                continue

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
    except Exception as e:
        handle_exception(bot=bot, e=e)
