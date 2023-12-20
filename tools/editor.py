import re
import string
from typing import List, Pattern, Text


def remove_emoji(text: Text) -> str:
    emoji_pattern: Pattern[Text] = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def remove_punct(text: Text) -> str:
    def ignore_chars(text: Text, ignose_list: List[str] = ["+", "@"]) -> str:
        for char in ignose_list:
            text = text.replace(char, "")
        return text

    result = remove_emoji(
        text.translate(
            str.maketrans("", "", ignore_chars(string.punctuation.join("«»")))
        )
    )
    return result


def make_plain(text: str) -> str:
    return remove_punct(" ".join(str(text).lower().splitlines()))
