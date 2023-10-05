from messages import Messages
from mind import Mind
from commands import CommandHandler, find_command

import openai
import psutil
from datetime import datetime


def retrieve_key():
    with open("key.txt", "r") as file:
        return file.read()


def main():
    messages = Messages()
    mind = Mind()
    command_handler = CommandHandler()

    openai.api_key = retrieve_key()

    await_reply = False
    while True:
        if not await_reply:
            # get system info
            battery = psutil.sensors_battery()

            sys_info = f"SYSTEM INFO [BATTERY LIFE: {battery.percent}%, " \
                       f"BATTERY CHARGING: {battery.power_plugged}, " \
                       f"SYSTEM TIME: {datetime.now()}]"
            chat_info = f"MESSAGE COUNT: {len(messages)}"
            messages.insert("system", sys_info + "\n" + chat_info)

            messages.insert("user", input("user: "))

        response = openai.ChatCompletion.create(
            model='gpt-4', # gpt-3.5-turbo
            messages=messages.all(),
            stream=True  # again, we set stream=True
        )

        collected_chunks = []
        role = "assistant"
        message = ""
        reply = False
        print("assistant:", end="")
        for chunk in response:
            collected_chunks.append(chunk)
            chunk_message = chunk['choices'][0]['delta']
            content = chunk_message.get("content", "")
            message += content
            if "[Reply]:" in message:
                reply = True
            if reply:
                print(content.replace("]:", ""), end="", flush=True)

        # print(message)
        messages.insert(role, message)
        mind.populate_from_message(message)
        cmd_type, cmd = find_command(message)
        if cmd_type and cmd:
            stdout = command_handler.run(cmd_type, cmd)
            if stdout:
                messages.insert("system", stdout)
        print("\n")
        print(mind)
        print(len(str(messages.all())))
        print()

        if mind.get_desire_to_continue():
            await_reply = True
        else:
            await_reply = False
            messages.filter(2000)


if __name__ == "__main__":
    main()
