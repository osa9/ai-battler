from typing import List

import openai


class AiBase:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def get_gpt_response(self, messages: List[object], trial: int = 3) -> str:
        for i in range(trial):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )

                return response["choices"][0]["message"]["content"]
            except Exception as e:
                if "Please reduce the length of the messages" in str(e):
                    raise Exception("入力が長すぎます。入力を短くして再度試してみて下さい")
                print(e)
                continue
        raise Exception("うまく動きませんでした。。入力を変えて再度試してみて下さい")
