import os
from discord_slash import SlashCommand
import discord
from discord_slash.utils.manage_commands import create_option
import urllib
import random

print('running bot in')
print(os.getcwd())

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path = os.path.join(os.path.dirname(__file__), '.env'))
except Exception:
    print("Unable to load dotenv, reverting to system environment variable") # dotenv is a bitch

ADMIN_ID = os.getenv("ADMIN_ID")
TOKEN = os.getenv("TOKEN")


client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

insults = []

data = urllib.request.urlopen("https://raw.githack.com/jbritain/InsultBot/main/src/insults.csv") # get insults from online list
for line in data:
    insults.append(line.decode("utf-8"))
    print(line.decode("utf-8")) # print all insults

@client.event
async def on_ready():

    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name="with your mother"))
    
@slash.slash(
name="Insult",
description="Insult someone",
options=[
    create_option(
        name="person",
        description="The person to insult",
        option_type=3,
        required=True
    )
]
)
async def insult(ctx, person): # insult someone
    if person == "@everyone":
        await ctx.send(random.choice(insults).replace("?1", ctx.author.mention).replace("?2", "everyone").replace("\"", "")) # if someone tries to insult everyone, insult them instead
    elif person.replace("!", "") == client.user.mention:
        await ctx.send(random.choice(insults).replace("?1", ctx.author.mention).replace("?2", client.user.mention).replace("\"", "")) # the bot cannot insult itself, that is a sign of weakness
    else:
        await ctx.send(random.choice(insults).replace("?1", person).replace("?2", ctx.author.mention).replace("\"", ""))

@slash.slash(
name="Reload",
description="Reload all commands (only specific users can use this command)",
)
async def reload(ctx): # reload all insults
    if str(ctx.author.id) == ADMIN_ID:
        await ctx.send("reloading insults...")
        ctx.defer()
        print(ctx.author.id)
        insults = []
        data = urllib.request.urlopen("https://raw.githack.com/Pr0x1mas/InsultBot/main/src/insults.csv") # get insults from online list
        i = 0
        for line in data:
            insults.append(line.decode("utf-8"))
            print("loaded insult " + line.decode("utf-8"))
            i += 1
        await ctx.send(str(i) + " insults loaded")
    else:
        await ctx.send("You do not have permission to do this")

@slash.slash(
name="Submit",
description="Submit a command",
options=[
    create_option(
        name="insult",
        description="The Insult to submit",
        option_type=3,
        required=True
    )
]
)
async def submit(ctx, insult):
    with open("submissions.txt", "a") as submissionList:
        submissionList.write(insult + "\n")
        await ctx.send("Insult submitted!")

client.run(TOKEN)
