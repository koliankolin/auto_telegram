import os
import sys
import traceback

from telebot import TeleBot, formatting


def handle_exception(bot: TeleBot, e: Exception):
    exception_type, exception_object, exception_traceback = sys.exc_info()
    exception_summary = traceback.extract_tb(exception_traceback)[0]
    alert_chat = os.environ.get("ALERT_CHAT")

    alert_message = f"""
Exception type: {exception_type}
Exception: {str(e)}
File: {exception_summary.filename}
Function name: {exception_summary.name}
Line number: {exception_summary.lineno}
Line with error: {exception_summary.line}
    """

    bot.send_message(
        chat_id=alert_chat,
        text=formatting.hpre(alert_message),
    )
