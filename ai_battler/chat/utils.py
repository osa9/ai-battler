import re


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean_a = re.compile("<a.*?>(.*?)</a>")
    clean_tag = re.compile("<.*?>")
    clean_emoji = re.compile(r":[^:\s]*:")
    text = re.sub(clean_a, "", text)
    text = re.sub(clean_tag, "", text)
    text = re.sub(clean_emoji, "", text)
    return text
