import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir_abs_path = os.path.join(abs_path, directory)
        norm_path = os.path.normpath(target_dir_abs_path)
        is_target_dir_valid = os.path.commonpath([abs_path, norm_path]) == abs_path

        if not is_target_dir_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(norm_path):
            return f'Error: "{directory}" is not a directory'

        output = ""
        for name in os.listdir(norm_path):
            full_path = os.path.join(norm_path, name)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            output += f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return output.rstrip()
        # return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'
