import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

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

        if author_id not in cooldowns or cooldowns[author_id] == 0:
            cooldowns[author_id] = 30
            await process_commands(message)
        else:
            await message.delete()
            await message.author.send(f"You are on cooldown. Please wait for {cooldowns[author_id]} seconds.")

    await decrease_cooldown(author_id)

async def decrease_cooldown(author_id):
    while cooldowns.get(author_id, 0) > 0:
        cooldowns[author_id] -= 1
        await asyncio.sleep(1)
    if author_id in cooldowns:
        del cooldowns[author_id]

async def process_commands(message):
    if not message.content.startswith('!'):
        return

    ctx = await client.get_context(message)
    if ctx.command is None:
        return

    try:
        await client.invoke(ctx)
    except commands.CommandError as error:
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            cooldown_seconds = round(cooldown)
            await ctx.author.send(f"You are on cooldown. Please wait for {cooldown_seconds} seconds.")

@client.command()
async def test(ctx):
    await ctx.send("This is a test command.")

client.run('YOUR_TOKEN')
