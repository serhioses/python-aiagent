import json
from openai import OpenAI
from call_function import available_functions, call_function
from functions.write_file import write_file

def generate_content(client: OpenAI, messages: list, verbose: bool) -> bool | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Failed to get usage object on response.")
    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    # write_file(".", "conversation.txt", f"{message.model_dump_json()}\n\n\n")
    messages.append(message)
    if not message.tool_calls:
        print(f"Final response:\n {message.content}")
        return True

    for tool_call in message.tool_calls:
        if tool_call.type == "function":
            result_message = call_function(tool_call, verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")
            if verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
            # write_file(".", "conversation.txt", f"{json.dumps(result_message)}\n\n\n")
            # function_args = json.loads(tool_call.function.arguments or "{}")
            # print(f"Calling function: {tool_call.function.name}({function_args})")

def filter_message(message):
    new_message = {}
    for key in message:
        if message[key] is None or callable(message[key]):
            continue
        new_message[key] = message[key]
    return new_message