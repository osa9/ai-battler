from typing import List, Union, Optional
from ai_battler.ai.base import AiBase
import openai
import json
import requests
from readability import Document
import html_text
import re
from pytube import extract, YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import validators

# prompt is inspired by https://chrome.google.com/webstore/detail/chatgpt-%C2%BB-summarize-every/cbgecfllfhmmnknmamkejadjmnmpfjmp?hl=ja
SYSTEM_PROMPT = """
Your output should use the following template:
- [Emoji] Bulletpoint

Your assignment is to summarize of given text that is web page content.
The summary should be up to five brief bullet points of the text I will give you.
Pick a suitable emoji for every bullet point.
Dot not add any text other than the bullet points and emojis, 
Your response should be in Japanese.
The text you will summarize is as follows:
{{CONTENT}}
"""

SYSTEM_PROMPT_YOUTUBE = """
Your output should use the following template:
- [Emoji] Bulletpoint

Your assignment is to summarize of given text that is youtube transcript.
The summary should be up to five brief bullet points of the text I will give you.
Pick a suitable emoji for every bullet point.
Dot not add any text other than the bullet points and emojis, 
Your response should be in Japanese.
The text you will summarize is as follows:
{{CONTENT}}
"""


class WebSummary(AiBase):
    def _extract_bullet_points(self, text: str) -> List[str]:
        print(text)
        res = []
        for line in text.split("\n"):
            m = re.match(r"-?\s*(.\s.+)", line)
            if m:
                res.append(m.group(1))
        return res

    def _get_youtube_video_id(self, url: str) -> Optional[str]:
        if (
            url.startswith("https://www.youtube.com/")
            or url.startswith("https://youtu.be/")
            or url.startswith("https://m.youtube.com/")
            or url.startswith("https://youtube.com/")
        ):
            extracted = extract.video_id(url)
            return extracted
        return None

    def _sec_to_min(self, sec: float) -> str:
        return f"{int(sec // 60)}:{int(sec % 60)}"

    def _get_youtube_content(self, video_id: str, url) -> str:
        transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja"])
        title = YouTube(url).title
        return (
            "Title: "
            + title
            + "\n".join(
                [f"[{self._sec_to_min(t['start'])}] {t['text']}" for t in transcripts]
            )
        )

    def _get_content(self, url: str) -> str:
        if not validators.url(url, public=True):
            raise Exception("URLが不正です")

        video_id = self._get_youtube_video_id(url)
        if video_id:
            try:
                content = self._get_youtube_content(video_id, url)
                return {"type": "youtube", "content": content}
            except Exception as e:
                return None
        else:
            response = requests.get(url)
            doc = Document(response.text)
            return {
                "type": "web",
                "title": doc.title(),
                "content": html_text.extract_text(doc.summary()),
            }

    def run(self, url: str) -> str:
        content = self._get_content(url)
        if content is None:
            return "コンテンツが取得できませんでした"

        if content["type"] == "web":
            title = content["title"]
            content = content["content"]
            prompt = SYSTEM_PROMPT.replace("{{TITLE}}", title).replace(
                "{{CONTENT}}", content
            )
        else:
            content = content["content"]
            prompt = SYSTEM_PROMPT_YOUTUBE.replace("{{CONTENT}}", content)

        messages = [
            {"role": "user", "content": prompt},
        ]
        return self.get_gpt_response(messages)


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()
    summary = WebSummary(api_key=os.getenv("OPENAI_API_KEY"))
    # print(summary.run("http://10.0.0.1"))
    print(
        summary.run(
            "https://www.youtube.com/watch?v=mRRd3wGkCnw&ab_channel=%E3%81%95%E3%81%8B%E3%81%BE%E3%81%9F%E6%B0%B4%E6%97%8F%E9%A4%A8%E3%80%90%E6%B2%99%E8%8A%B1%E5%8F%89%E3%82%AF%E3%83%AD%E3%83%B1%F0%9F%8E%A3%2C%E3%83%9B%E3%83%AD%E3%83%A9%E3%82%A4%E3%83%96%2C%E5%88%87%E3%82%8A%E6%8A%9C%E3%81%8D%E3%80%91"
        )
    )
