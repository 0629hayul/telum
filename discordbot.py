from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
from datetime import timedelta

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
cooldown_dict = {}
#cooldown_time = datetime.timedelta(seconds=86400)

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')
    cooldown_time = timedelta(hours=24)  # 쿨다운 시간

    if message.channel.id == 1109828429261590669:
        author_id = str(message.author.id)
        now = datetime.now()

        if author_id in cooldown_dict and cooldown_dict[author_id] > now:
            await message.delete()
            return

        cooldown_dict[author_id] = now + cooldown_time

    await client.process_commands(message)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
