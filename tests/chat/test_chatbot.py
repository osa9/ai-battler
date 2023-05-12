import unittest
from ai_battler.chat.chatbot import ChatBot
from ai_battler.ai.arena import Arena

import dotenv
import os

dotenv.load_dotenv()


class ChatBotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chatbot = ChatBot(Arena(api_key=os.getenv("OPENAI_API_KEY")))

    def test_parse(self):
        s = "回避特化ゴリラ vs 絶対に何をも貫く槍"
        res = self.chatbot._parse_text(s)
        self.assertEqual(
            res, {"operation": "battle", "players": ["回避特化ゴリラ", "絶対に何をも貫く槍"]}
        )

    def test_parse_no_space(self):
        s = "回避特化ゴリラ vs 絶対に何をも貫く槍"
        res = self.chatbot._parse_text(s)
        print(res)
        self.assertEqual(
            res, {"operation": "battle", "players": ["回避特化ゴリラ", "絶対に何をも貫く槍"]}
        )

    def test_battle(self):
        s = "姫騎士 vs オーク"
        res = self.chatbot.action("", s)
        print(res)


if __name__ == "__main__":
    unittest.main()
