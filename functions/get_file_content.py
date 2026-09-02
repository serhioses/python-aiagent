import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.join(abs_path, file_path)
        norm_path = os.path.normpath(file_abs_path)
        is_target_file_path_valid = os.path.commonpath([abs_path, norm_path]) == abs_path

        if not is_target_file_path_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(norm_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(norm_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
