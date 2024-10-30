import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ollama

import constants
import tts_local
from ollama import AsyncClient

from commandlist import CommandList
from custom_commands import find_all
from weather_api import get_weather_city


async def chat():
    commands = CommandList()
    model = "llama3.2"
    context = []
    await communicate(constants.HELLO_PROMPT, context, model)
    while True:
        prompt = input("\n> ")
        lower_prompt = prompt.lower().strip()
        if lower_prompt == 'danke':
            await communicate(constants.GOODBYE_PROMPT, context, model)
            return

        elif lower_prompt in commands.find:
            context = await search_and_open_file(context, model)

        elif lower_prompt in commands.weather:
            context = await get_weather_data(context, model)

        else:
            context = await communicate(prompt, context, model)

async def communicate(prompt, context, model):
    try:
        response = await AsyncClient().generate(model='HiveAI', prompt=prompt, context=context)
        print(response['response'])
        tts_local.speak(response['response'])
        for part in response['context']:
            context.append(part)
    except ollama.ResponseError as e:
        print(f"Error: {e.error}")
        if e.status_code == 404:
            ollama.pull(model)
    finally:
        return context

async def search_and_open_file(context, model):
    context = await communicate(constants.SEARCH_FILE_PROMPT, context, model)
    to_find = input('>> ')

    result = []

    result = find_all(to_find)

    with ThreadPoolExecutor() as executor:
        for rv in executor.map(find_all, to_find, next(os.walk(Path.home()))[1]):
            result.extend(rv)

    if not result:
        context = await communicate(to_find + ' nicht gefunden', context, model)
    else:
        if len(result) > 1:
            context = await communicate('Folgende Dateien wurden gefunden:' + result, context, model)
        else:
            context = await communicate(constants.FILE_FOUND_PROMPT + ' ' + result[0], context, model)
            open_file = input('[Y/N] >> ')
            match open_file.lower():
                case 'y':
                    context = await communicate(constants.OPEN_FILE, context, model)
                    os.startfile("\\".join(result[0].split('\\')[:-1]))
                case 'n':
                    context = await communicate(constants.NOT_OPEN_FILE, context, model)
                case _:
                    pass
    return context

async def get_weather_data(context, model):
    context = await communicate(constants.WHICH_CITY_PROMPT, context, model)
    city = input('>> ')
    weather_data = get_weather_city(city)
    context = await communicate(json.dumps(weather_data), context, model)
    return context