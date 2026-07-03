import discord
from discord.ext import commands, tasks
import os
import asyncio

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1367543413808955422

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    join_voice.start()


@tasks.loop(seconds=10)
async def join_voice():
    await bot.wait_until_ready()

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel is None:
        print("Canal não encontrado")
        return

    vc = discord.utils.get(bot.voice_clients, guild=channel.guild)

    if vc is None or not vc.is_connected():
        try:
            await channel.connect()
            print("Entrou na call")
        except Exception as e:
            print("Erro ao entrar:", e)


bot.run(TOKEN)
