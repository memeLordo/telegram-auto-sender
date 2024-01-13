from typing import AnyStr


def convert_to_string_format(input_file_path: AnyStr) -> None:
    try:
        # Чтение содержимого файла
        with open(input_file_path, "r", encoding="utf-8") as file:
            while True:
                line = file.readline()
                if len(line) > 80:
                    print(repr(line[:60]))
                    print(repr(line[60:]))
                    continue
                if not line:
                    break
                print(repr(line))

        # Преобразование формата для переменной типа string

    except FileNotFoundError:
        print(f"Файл '{input_file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
