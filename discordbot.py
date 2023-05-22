import discord
from discord.ext import commands
import asyncio
from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import time
import datetime

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
client = discord.Client(intents=intents)
cooldowns = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 1109828429261590669:  # 특정 체널 ID
        author_id = message.author.id

        if author_id not in cooldowns or cooldowns[author_id] <= datetime.now():
            cooldowns[author_id] = datetime.now() + timedelta(seconds=30)
            await process_commands(message)
        else:
            await message.delete()
            cooldown_remaining = cooldowns[author_id] - datetime.now()
            await message.author.send(f"You are on cooldown. Please wait for {cooldown_remaining.total_seconds():.0f} seconds.")



try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
