import unittest
from ai_battler.chat.chatbot import ChatBot
from ai_battler.ai.arena import Arena
from ai_battler.ai.haiku import Haiku
from ai_battler.ai.summary import WebSummary

import dotenv
import os

dotenv.load_dotenv()


class ChatBotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chatbot = ChatBot(
            arena=Arena(api_key=os.getenv("OPENAI_API_KEY")),
            haiku=Haiku(api_key=os.getenv("OPENAI_API_KEY")),
            summary=WebSummary(api_key=os.getenv("OPENAI_API_KEY")),
        )

    def test_haiku(self):
        s = "俳句\nせんべいHDはインフレ率以上の給料アップしてるからな"
        res = self.chatbot.action("", s)
        print(res)
        self.assertEqual("詠んでみました。", res.split("\n")[0].strip())

    def test_multiplayer(self):
        s = "a vs b vs cvsd VS e vsぐああvsぐあ vs vs d"
        res = self.chatbot._parse_text(s)
        self.assertEqual(
            res,
            {
                "operation": "battle",
                "players": ["a", "b", "cvsd", "e", "ぐああ", "ぐあ", "d"],
                "type": None,
            },
        )

    def test_non_vs(self):
        s = "hello"
        res = self.chatbot._vs_players(s)
        self.assertEqual(res, None)

    def test_parse(self):
        s = "回避特化ゴリラ vs 絶対に何をも貫く槍"
        res = self.chatbot._parse_text(s)
        self.assertEqual(
            res,
            {"operation": "battle", "players": ["回避特化ゴリラ", "絶対に何をも貫く槍"], "type": None},
        )

    def test_parse_no_space(self):
        s = "回避特化ゴリラvs 絶対に何をも貫く槍"
        res = self.chatbot._parse_text(s)
        print(res)
        self.assertEqual(
            res,
            {"operation": "battle", "players": ["回避特化ゴリラ", "絶対に何をも貫く槍"], "type": None},
        )

    def test_summary(self):
        s = "要約\nhttps://www.youtube.com/watch?v=43YF4jBL0rE&ab_channel=%E3%81%B6%E3%81%84%E3%81%AE%E5%88%87%E3%82%8A%E6%8A%9C%E3%81%8D%E7%8C%AB"
        res = self.chatbot.action("", s)
        print(res)


if __name__ == "__main__":
    unittest.main()
