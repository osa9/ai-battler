import re


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean_a = re.compile("<a.*?>(.*?)</a>", re.MULTILINE)
    clean_tag = re.compile("<.*?>", re.MULTILINE)
    clean_emoji = re.compile(r":[^:\s]*:", re.MULTILINE)
    text = re.sub("<br />", "\n", text)
    text = re.sub(clean_a, "", text)
    text = re.sub(clean_tag, "", text)
    text = re.sub(clean_emoji, "", text)
    return text
