import string


def remove_punct(text):
    result = text.translate(
        str.maketrans("", "", (string.punctuation).replace("+", ""))
    )
    return result
