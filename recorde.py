import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1367543413808955422

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def join_voice():
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Canal não encontrado")
        return

    vc = discord.utils.get(bot.voice_clients)

    # se não existe conexão OU desconectou de verdade
    if vc is None or not vc.is_connected():
        try:
            await channel.connect(reconnect=True)
            print("Entrou na call")
        except Exception as e:
            print("Erro ao entrar:", e)

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    await join_voice()
    monitor.start()

@tasks.loop(seconds=10)
async def monitor():
    vc = discord.utils.get(bot.voice_clients)

    # se caiu da call → reconecta
    if vc is None or not vc.is_connected():
        print("Detectei queda da call, reconectando...")
        await join_voice()
