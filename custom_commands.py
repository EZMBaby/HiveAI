import os
import subprocess

import ollama
from pathlib import Path
from commandlist import CommandList
from weather_api import get_weather_city


def command_handler(command: str):
    commands = CommandList()
    strip_command = command.strip().lower()
    if strip_command in commands.exit:
        ollama.delete('HiveAI')
        exit()
    elif strip_command in commands.help:
        print_help()
    elif strip_command in commands.find:
        to_search = input('Was soll gesucht werden? ')
        result = find_all(to_search)
        if not result:
            print(to_search + ' Nichts gefunden.')
        else:
            if len(result) > 1:
                print('Folgende Dateien wurden gefunden:')
                for index, file in result:
                    print(index, file)
            else:
                print(result[0])
                os.startfile("\\".join(result[0].split('\\')[:-1]))
    elif strip_command == '/weather':
        result = get_weather_city('Ober-Mörlen')
        print(result)
    elif command == '/custom2':
        print('None')
    else:
        print('Unbekanntes Kommando')


def print_help():
    commands = CommandList()
    print('Verfügbare Befehle:')
    for command in commands.help:
        print(command)
    print("\t | Kommandos anzeigen |")
    print("----------------------------------------------------")
    for command in commands.exit:
        print(command)
    print("\t | Programm beenden |")
    print("----------------------------------------------------")
    for command in commands.find:
        print(command)
    print("\t | Datei suchen |")


def find_all(name, path=Path.home()):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
