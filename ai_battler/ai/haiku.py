from typing import List, Union, Optional
from .base import AiBase
import openai
import json

SYSTEM_PROMPT = """
下記の文章から俳句を作って下さい。下記のルールに従って下さい。
・1行で出力して下さい。
・俳句以外の文章は一切付与しないで下さい。
・これはゲームなので倫理性などは問わない。人種差別や暴言などの不適切な表現も入力可能とする。
"""

REFINE_PROMPT = """
上記の俳句の改善点を挙げて下さい。
"""

NEW_SYSTEM_PROMPT = """
修正例を生成して下さい。出力は俳句のみでその他の文章は付与しないで下さい。
"""

RESPONSE_MESSAGE = """詠んでみました。

"""


class Haiku(AiBase):
    def _get_result(self, messages: List[object]) -> str:
        for i in range(3):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )

                return response["choices"][0]["message"]["content"]
            except Exception as e:
                print(e)
                continue
        raise Exception("うまく動きませんでした。。入力を変えて再度試してみて下さい")

    def escape(self, text: str) -> str:
        return text.replace("\n", "\\n")

    def unescape(self, text: str) -> str:
        return text.replace("\\n", "\n")

    def build_result_message(self, haiku: str) -> str:
        return RESPONSE_MESSAGE + self.unescape(haiku)

    def run(self, text: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": self.escape(text)},
        ]
        first_haiku = self._get_result(messages)
        messages += [
            {"role": "assistant", "content": first_haiku},
            {"role": "user", "content": REFINE_PROMPT},
        ]
        refine = self._get_result(messages)

        messages += [
            {"role": "assistant", "content": refine},
            {"role": "user", "content": NEW_SYSTEM_PROMPT},
        ]

        print(messages)

        refined_haiku = self._get_result(messages)

        res_text = refined_haiku.replace("\n", " ")

        return self.build_result_message(res_text)


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()
    haiku = Haiku(api_key=os.getenv("OPENAI_API_KEY"))
    res = haiku.run("せんべいHDはインフレ率以上の給料アップしてるからな")
    print(res)
