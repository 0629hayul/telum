from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import asyncio
from datetime import datetime, timedelta
import datetime

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
msg_ed = {}
channel_id = 1109828429261590669

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    now = datetime.now()

    if user_id in msg_ed and msg_ed[user_id] == 1:
        await message.delete()
        return

    msg_ed[user_id] = 1
    await client.process_commands(message)
    
   
# 매일 오전 1시에 유저별 메시지 보낸 여부 초기화
async def reset_msg_ed():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.datetime.now()
        if now.hour == 1 and now.minute == 0:
            msg_ed.clear()
        await asyncio.sleep(60)  # 60초(1분)마다 반복
        
        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
