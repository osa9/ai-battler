import re


# example input
# <p><span class="h-card"><a href="https://handon.club/@ai" class="u-url mention">@<span>ai</span></a></span> 俳句</p><p>こんにちは<br />僕ようじょ</p>


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean_a = re.compile("<a.*?>(.*?)</a>", re.MULTILINE)
    clean_tag = re.compile("<.*?>", re.MULTILINE)
    clean_emoji = re.compile(r":[^:\s]*:", re.MULTILINE)
    text = re.sub("<br />", "\n", text)
    text = re.sub("</p>", "\n", text)
    text = re.sub(clean_a, "", text)
    text = re.sub(clean_tag, "", text)
    text = re.sub(clean_emoji, "", text)
    return text
