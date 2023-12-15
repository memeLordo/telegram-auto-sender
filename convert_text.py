def convert_to_string_format(input_file_path):
    try:
        # Чтение содержимого файла
        with open(input_file_path, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                print(repr(line))

        # Преобразование формата для переменной типа string

    except FileNotFoundError:
        print(f"Файл '{input_file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования
input_file_path = 'input.txt'

convert_to_string_format(input_file_path)
