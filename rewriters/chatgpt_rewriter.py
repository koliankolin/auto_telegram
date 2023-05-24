import os
import logging

import openai


class ChatGPTRewriter:
    def rewrite_title(self, title: str) -> str:
        logging.info(f"Original title: {title}")

        return self._request(
            f"rewrite text as title of article"
            f"in one sentence and send only new version"
            f"without mention that it is a new version please.\n\n{title}"
        )

    def rewrite_summary(self, summary: str) -> str:
        logging.info(f"Original summary: {summary}")

        return self._request(
            f"rewrite text as summary and keep only main idea"
            f"and send only new version"
            f"without mention that it is a new version please.\n\n{summary}"
        )

    @staticmethod
    def _request(request_message: str) -> str:
        token = os.environ.get("CHATGPT_TOKEN")
        openai.api_key = token

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role': 'user',
                'content': request_message
            }]
        )

        return completion.choices[0].message.content.strip()
