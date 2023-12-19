import os

from .convert_text import convert_to_string_format

dir_path = os.path.dirname(os.path.abspath(__file__))
input_file_path = dir_path + "/input.txt"
convert_to_string_format(input_file_path)
