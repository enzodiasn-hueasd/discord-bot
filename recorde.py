import discord
from discord.ext import commands, tasks
import os
import asyncio

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1367543413808955422

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def join_voice():
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            channel = bot.get_channel(VOICE_CHANNEL_ID)

            if channel is None:
                print("Canal não encontrado")
                await asyncio.sleep(10)
                continue

            vc = discord.utils.get(bot.voice_clients, guild=channel.guild)

            if vc is None or not vc.is_connected():
                print("Entrando na call...")
                await channel.connect()
            else:
                print("Já está na call")

        except Exception as e:
            print("Erro:", e)

        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")


class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(join_voice())

bot.run(TOKEN)
