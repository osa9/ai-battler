from typing import List

from ..ai.arena import Arena
from ..ai.haiku import Haiku
from ..ai.summary import WebSummary
import re


class ChatBot:
    def __init__(self, arena: Arena, haiku: Haiku, summary: WebSummary):
        self.arena = arena
        self.haiku = haiku
        self.summary = summary

    def _escape_player(self, player: str) -> str:
        return player.strip()

    def _remove_mention(self, text: str) -> str:
        return re.sub(r"@ai", "", text).strip()

    def _vs_players(self, text: str) -> List[str]:
        players = re.split("(?<=[^a-zA-Z0-9])(?:vs|VS)(?=[^a-zA-Z0-9])", text)
        valid_players = [
            self._escape_player(player)
            for player in players
            if len(self._escape_player(player)) > 0
        ]
        if len(valid_players) > 1:
            return valid_players
        else:
            return None

    def _parse_text(self, text: str):
        lines = text.split("\n")
        if len(lines) >= 2:
            print(lines[0])
            print(lines[1])
            battle_type = lines[0].strip()
            if battle_type == "俳句" or battle_type.lower() == "haiku":
                return {"operation": "haiku", "message": "\n".join(lines[1:])}
            if battle_type == "要約" or battle_type == "まとめて":
                return {"operation": "summary", "url": lines[1]}
            players = self._vs_players(lines[1])
            if players:
                return {"operation": "battle", "players": players, "type": battle_type}
        # A vs B
        players = self._vs_players(text)
        if players:
            return {"operation": "battle", "players": players, "type": None}
        # Challenge match
        return {"operation": "challenge", "player": self._remove_mention(text)}

    def action(self, account_id, text):
        ops = self._parse_text(text)
        print(text)
        print(ops)

        if ops["operation"] == "notion":
            return ops["message"]
        elif ops["operation"] == "battle":
            result = self.arena.battle(ops["players"], ops["type"])
            return self.arena.build_result_message(result, ops["type"])
        elif ops["operation"] == "summary":
            return self.summary.run(ops["url"])
        elif ops["operation"] == "haiku":
            return self.haiku.run(ops["message"])
        else:
            return None
