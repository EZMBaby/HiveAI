import asyncio
import os

import ollama
import constants
from ai_functions import chat
from commandlist import CommandList
from custom_commands import command_handler, find_all
from model_data import modelfile


if __name__ == '__main__':
    commands = CommandList()
    ollama.create(model='HiveAI', modelfile=modelfile)
    while True:
        user_input = input('\n-> ')
        if user_input == 'Hey HiveAI':
            asyncio.run(chat())
        else:
            command_handler(user_input)
