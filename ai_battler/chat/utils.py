import re


# example input
# <p><span class="h-card"><a href="https://handon.club/@ai" class="u-url mention">@<span>ai</span></a></span> 俳句</p><p>こんにちは<br />僕ようじょ</p>
# "\u003cp\u003eこれって\u003cbr /\u003e\u003ca href=\"https://www.nikkei.com/article/DGXZQOUA2994G0Z20C23A5000000/\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"\u003e\u003cspan class=\"invisible\"\u003ehttps://www.\u003c/span\u003e\u003cspan class=\"ellipsis\"\u003enikkei.com/article/DGXZQOUA299\u003c/span\u003e\u003cspan class=\"invisible\"\u003e4G0Z20C23A5000000/\u003c/span\u003e\u003c/a\u003e\u003c/p\u003e\u003cp\u003eこういうサイトをやめろってこと？\u003cbr /\u003e\u003ca href=\"https://www3.nhk.or.jp/news/\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"\u003e\u003cspan class=\"invisible\"\u003ehttps://\u003c/span\u003e\u003cspan class=\"\"\u003ewww3.nhk.or.jp/news/\u003c/span\u003e\u003cspan class=\"invisible\"\u003e\u003c/span\u003e\u003c/a\u003e\u003c/p\u003e"


def extract_link(text):
    m = re.search(r"<a href=\"(.*?)\"[^>]*?target=\"_blank\"[^>]*?>(.*?)</a>", text)
    if m:
        return m.group(1)
    return None


def remove_html_tags(text):
    """Remove html tags from a string"""
    text = re.sub("<br />", "\n", text)
    text = re.sub("</p>", "\n", text)
    lines = text.split("\n")
    if len(lines) > 1:
        link = extract_link(lines[1])

    clean_a = re.compile("<a.*?>(.*?)</a>", re.MULTILINE)
    clean_tag = re.compile("<.*?>", re.MULTILINE)
    clean_emoji = re.compile(r":[^:\s]*:", re.MULTILINE)

    text = re.sub(clean_a, "", text)
    text = re.sub(clean_tag, "", text)
    text = re.sub(clean_emoji, "", text)
    if link:
        lines = text.split("\n")
        lines[1] = link
        text = "\n".join(lines)

    return text


if __name__ == "__main__":
    x = '\u003cp\u003eこれって\u003cbr /\u003e\u003c<a href="https://www.nikkei.com/article/DGXZQOUA2994G0Z20C23A5000000/" target="_blank" rel="nofollow noopener noreferrer">\u003e\u003cspan class="invisible"\u003ehttps://www.\u003c/span\u003e\u003cspan class="ellipsis"\u003enikkei.com/article/DGXZQOUA299\u003c/span\u003e\u003cspan class="invisible"\u003e4G0Z20C23A5000000/\u003c/span\u003e\u003c/a\u003e\u003c/p\u003e\u003cp\u003eこういうサイトをやめろってこと？\u003cbr /\u003e\u003ca href="https://www3.nhk.or.jp/news/" target="_blank" rel="nofollow noopener noreferrer"\u003e\u003cspan class="invisible"\u003ehttps://\u003c/span\u003e\u003cspan class=""\u003ewww3.nhk.or.jp/news/\u003c/span\u003e\u003cspan class="invisible"\u003e\u003c/span\u003e\u003c/a\u003e\u003c/p\u003e'
    print(remove_html_tags(x))
