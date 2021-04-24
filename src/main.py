from discord.ext import commands
import discord
import os

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path = os.path.join(os.path.dirname(__file__), '.env'))
except Exception:
    print("Unable to load dotenv, reverting to system environment variable") # dotenv is a bitch

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='?', description='Insult your friends with InsultBot, or suggest your own insults!')

bot.load_extension("insultCommands")

@bot.event
async def on_ready():
    print('running bot in')
    print(os.getcwd())
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)