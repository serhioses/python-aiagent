import os
from openai.types.chat import ChatCompletionFunctionToolParam

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(abs_working_dir, exist_ok=True)
        with open(abs_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'

schema_write_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes into a file from the working directory. The requested file path must resolve to a location inside the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write content into, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to be written into a given file",
                },
            },
        },
    },
}
