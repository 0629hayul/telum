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

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
cooldown_time = datetime.timedelta(hours=24)
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
        today = datetime.date.today()

        # 사용자별로 남은 시간을 저장하기 위한 딕셔너리
        cooldown_dict = {}

        # 만약 사용자 ID가 딕셔너리에 있다면
        if author_id in cooldown_dict:
            last_sent = cooldown_dict[author_id]

            # 이미 메시지를 보낸 경우
            if last_sent == today:
                # 메시지 삭제
                await message.delete()
                # 제한 시간 계산
                remaining_time = (datetime.datetime.now() + cooldown_time) - datetime.datetime.now()
                # DM으로 알림 전송
                dm_message = f"1일 1회 제한 (남은시간: {remaining_time})"
                await message.author.send(dm_message)
                return

        # 처음 메시지를 보낸 경우
        # 관리자가 확인할 수 있도록 원하는 작업을 수행하고, 이 부분은 알맞게 수정해야 합니다.
        # 여기서는 관리자가 해당 메시지를 확인한다고 가정하고, 콘솔에 출력합니다.
        print(f"New message: {message.content}")

        # 딕셔너리에 사용자 ID와 오늘 날짜 저장
        cooldown_dict[author_id] = today

        await client.process_commands(message)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
