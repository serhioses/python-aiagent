import json
from collections.abc import Callable
from openai.types.chat import ChatCompletionMessageFunctionToolCall
from config import WORKING_DIR
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(tool_call: ChatCompletionMessageFunctionToolCall, verbose: bool = False) -> dict:
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    if func_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {func_name}",
        }
    func_args["working_directory"] = WORKING_DIR
    result = function_map[func_name](**func_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
