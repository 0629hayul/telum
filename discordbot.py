from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import time
import asyncio
from datetime import timedelta
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
cooldowns = {}
#cooldown_time = datetime.timedelta(seconds=86400)

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == 1109828429261590669:  # 특정 체널 ID
        author_id = message.author.id

        if author_id not in cooldowns or cooldowns[author_id] == 0:
            cooldowns[author_id] = 30
            await process_commands(message)
        else:
            await message.delete()
            await message.author.send(f"You are on cooldown. Please wait for {cooldowns[author_id]} seconds.")

    cooldown_task = asyncio.create_task(decrease_cooldown(author_id))
    await cooldown_task
async def decrease_cooldown(author_id):
    while cooldowns.get(author_id, 0) > 0:
        cooldowns[author_id] -= 1
        await time.sleep(1)
    if author_id in cooldowns:
        del cooldowns[author_id]

async def process_commands(message):
    if not message.content.startswith('!'):
        return

    ctx = await client.get_context(message)
    if ctx.command is None:
        return

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
