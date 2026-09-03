from dotenv import load_dotenv
load_dotenv()

import sys
import json
from prompts import system_prompt
from config import MAX_MESSAGE_ITERS
from agent.arg_parser import create_arg_parser
from agent.openai_client import create_openai_client
from agent.content import generate_content
from functions.write_file import write_file

def main():
    # with open("conversation.txt", "w") as file:
    #     file.write("")

    args = create_arg_parser()
    client = create_openai_client()
    # write_file('.', 'conversation.txt', f'{json.dumps({"role": "system", "content": system_prompt})}\n\n\n')
    # write_file('.', 'conversation.txt', f'{json.dumps({"role": "user", "content": args.user_prompt})}\n\n\n')
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_MESSAGE_ITERS):
        try:
            if generate_content(client, messages, args.verbose):
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_MESSAGE_ITERS}) reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
