import openai


class AiBase:
    def __init__(self, api_key: str):
        openai.api_key = api_key
