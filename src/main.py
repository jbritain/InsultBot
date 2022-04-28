import os
from discord_slash import SlashCommand
import discord
from discord_slash.utils.manage_commands import create_option
import urllib
import random
import csv

print('running bot in' + os.getcwd())
try:
    os.chdir("src") # why does vscode insist on running in the root directory
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path = os.path.join(os.path.dirname(__file__), '.env'))
except Exception:
    print("Unable to load dotenv, reverting to system environment variable") # dotenv is a bitch

ADMIN_ID = os.getenv("ADMIN_ID")
TOKEN = os.getenv("TOKEN")
if(os.getenv("MAINTENENCE_MODE") == "True"):
    MAINENTENCE_MODE = True
else:
    MAINENTENCE_MODE = False


client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

insults = []
try:
    data = urllib.request.urlopen("https://raw.githack.com/jbritain/InsultBot/main/src/insults.csv") # get insults from online list
    for line in data:
        insults.append(line.decode("utf-8").replace("\"", ""))
        print(line.decode("utf-8").replace("\"", "")) # print all insults
except Exception:
    print("Unable to fetch insult list, resorting to local copy")

    with open("insults.csv") as dataFile:
        reader = csv.reader(dataFile, delimiter=',', quoting=csv.QUOTE_ALL)
        for line in reader:
            insults.append(line[0].replace("\"", ""))
            print(line[0].replace("\"", ""))

@client.event
async def on_ready():

    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    if MAINENTENCE_MODE:
        await client.change_presence(activity=discord.CustomActivity("Undergoing maintenence"))
    else:
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
        await ctx.send(random.choice(insults).replace("?1", ctx.author.mention).replace("?2", "everyone")) # if someone tries to insult everyone, insult them instead
    elif person.replace("!", "") == client.user.mention or person.replace("", "!") == ctx.guild.get_member(int(ADMIN_ID)).mention:
        await ctx.send(random.choice(insults).replace("?1", ctx.author.mention).replace("?2", client.user.mention)) # the bot cannot insult itself or the creator of the bot, that is a sign of weakness
    else:
        await ctx.send(random.choice(insults).replace("?1", person).replace("?2", ctx.author.mention))

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
        try:
            data = urllib.request.urlopen("https://raw.githack.com/Pr0x1mas/InsultBot/main/src/insults.csv") # get insults from online list
        except Exception:
            await ctx.send("Error loading insults")
            return 0
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
