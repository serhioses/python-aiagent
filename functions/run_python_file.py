import os
import subprocess
from openai.types.chat import ChatCompletionFunctionToolParam

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output: list[str] = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stderr and not completed_process.stdout:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file from the working directory with an optional list of arguments (strings) as command-line arguments. The requested file path must resolve to a location inside the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of command-line arguments to pass to the Python file.",
                },
            },
        },
    },
}
