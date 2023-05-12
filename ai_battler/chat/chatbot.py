from ..ai.arena import Arena
import re


class ChatBot:
    def __init__(self, arena: Arena):
        self.arena = arena

    def _escape_player(self, player: str) -> str:
        return player.strip()

    def _remove_mention(self, text: str) -> str:
        return re.sub(r"@ai", "", text).strip()

    def _parse_text(self, text: str):
        # A vs B
        match = re.match(r"(.*[^a-zA-Z0-9])vs([^a-zA-Z0-9].*)", text, re.IGNORECASE)
        if match:
            a = self._escape_player(match.group(1))
            b = self._escape_player(match.group(2))
            if len(a) > 0 and len(b) > 0:
                return {"operation": "battle", "players": [a, b]}
        # Challenge match
        return {"operation": "challenge", "player": self._remove_mention(text)}

    def action(self, account_id, text):
        ops = self._parse_text(text)
        print(text)
        print(ops)

        if ops["operation"] == "notion":
            return ops["message"]
        if ops["operation"] == "battle":
            result = self.arena.battle(ops["players"])
            return self.arena.build_result_message(result)
        if ops["operation"] == "challenge":
            # TODO: Implement
            return None
