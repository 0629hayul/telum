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
    for guild in client.guilds:
        for member in guild.members:
            msg_ed[member.id] = 0
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!e'):
        if message.author.id == 819436785998102548:
            split = message.content.split()
            if len(split) == 2 and split[0] == '!e':
                try:
                    limit = int(split[1])
                    if limit < 1 or limit > 1000:
                        raise ValueError
                except ValueError:
                    await message.channel.send('ValueError')
                    return
                deleted = await message.channel.purge(limit=limit)
                
    if message.channel.id == 1109828429261590669:
        now = datetime.now()
        end_of_today = datetime(now.year, now.month, now.day, 23, 59, 59)
        remaining_time = end_of_today - now
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds // 60) % 60
        usr = message.author
        msged = msg_ed.get(usr.id, 0)
        if msged == 0:
            await message.channel.send("callback!")
            msged = 1
        elif msged == 1:
            embedVar = discord.Embed(title="무료에딧 실패", color=0x00ff26)
            embedVar.add_field(name="",value=f"오늘 이미 무료에딧을 사용했습니다.({hours}시간 {minutes}분 후에 가능)",inline=False)
            embedVar.add_field(name="",value="- <#1107973988862402632>시 무료에딧 **한번에 2가지 옵션 가능**",inline=False)
            embedVar.add_field(name="",value="- 구매는 __무제한__입니다. ---- 옵션 : <#1079005959873110076>",inline=False)
            await message.auther.send(embed=embedVar)
        else:
            await message.channel.send(f"* **관리자에게 문의해주세요** \n알 수 없는 오류\ned 코드 :{msged}")    
# 매일 오전 1시에 유저별 메시지 보낸 여부 초기화
async def reset_msg_ed():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.datetime.now()
        if now.hour == 1 and now.minute == 0:
            for guild in client.guilds:
                for member in guild.members:
                    msg_ed[member.id] = 0
        await asyncio.sleep(60)  # 60초(1분)마다 반복
        
        
try:
    client.loop.create_task(reset_msg_ed())
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
