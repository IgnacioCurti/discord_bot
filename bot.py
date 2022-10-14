import os
import discord
from dotenv import load_dotenv
import logging
from services import get_matches_by_date
from random import  choice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        greeting = choice(["Hi", "Hello", "Hey"])
        await message.channel.send(f'{greeting} {message.author.display_name}!')

    if message.content.startswith('!matches'):
        try:
            date = message.content.split(" ")[1]
        except IndexError:
            date = ""
        await message.channel.send(get_matches_by_date(date))


@client.event
async def on_message_edit(before, after):
    await before.channel.send(f'Soy un botón pero {before.author.display_name} había escrito "{before.content}"')


client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)