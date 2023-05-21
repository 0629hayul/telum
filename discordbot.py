from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import datetime

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
cooldown_dict = {}
cooldown_time = datetime.timedelta(seconds=86400)

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
    if message.channel.id == 1109828429261590669:
        author_id = str(message.author.id) 
        today = datetime.datetime.now().date() #

        # 사용자가 처음 메시지를 보내는 경우 또는 제한 시간이 지난 경우
        if author_id not in cooldown_dict or cooldown_dict[author_id] < today:
            cooldown_dict[author_id] = 86400
            # 관리자가 확인할 수 있도록 원하는 작업을 수행하고, 이 부분은 알맞게 수정해야 합니다.
            # 여기서는 관리자가 해당 메시지를 확인한다고 가정하고, 콘솔에 출력합니다.
            print(f"New message: {message.content}")
        else:
            # 이미 메시지를 보낸 경우
            await message.delete()
            # 제한 시간 계산
            remaining_time_seconds = (datetime.datetime.combine(cooldown_dict[author_id], datetime.time.max) + cooldown_time) - datetime.datetime.now()
            remaining_time_hours = int(remaining_time_seconds.total_seconds() // 3600)
            remaining_time_minutes = int((remaining_time_seconds.total_seconds() % 3600) // 60)
            remaining_time = f"{remaining_time_hours}시간 {remaining_time_minutes}분"
            # DM으로 알림 전송
            dm_message = f"1일 1회 제한 (남은시간: {remaining_time})"
            await message.author.send(dm_message)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
