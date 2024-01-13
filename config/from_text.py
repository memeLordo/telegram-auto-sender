def read_add_message() -> str:
    with open("config/script.txt", "r+", encoding="utf-8") as file:
        return file.read()
