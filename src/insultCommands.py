from discord.ext import commands
import discord
import random
import urllib

class insultCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.insults = []
        data = urllib.request.urlopen("https://pr0x1mas.github.io/InsultBot/src/insults.csv") # get insults from online list
        for line in data:
            self.insults.append(line.decode("utf-8"))
            print(line.decode("utf-8")) # print all insults
        


    @commands.command(brief="Insult someone", description="Insult someone in the format `?insult @user-to-insult`")
    async def insult(self, ctx, person):
        if person == "@everyone":
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", "everyone").replace("\"", "")) # if someone tries to insult everyone, insult them instead
        elif person.replace("!", "") == self.bot.user.mention:
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", self.bot.user.mention).replace("\"", "")) # the bot cannot insult itself, that is a sign of weakness
        else:
            await ctx.send(random.choice(self.insults).replace("?1", person).replace("?2", ctx.author.mention).replace("\"", ""))

    @commands.command()
    async def reload(self, ctx): # reload all insults
        await ctx.send("reloading insults...")
        async with ctx.typing():
            self.insults = []
            data = urllib.request.urlopen("https://pr0x1mas.github.io/InsultBot/src/insults.csv") # get insults from online list
            for line in data:
                self.insults.append(line.decode("utf-8"))
                print("loaded insult " + line.decode("utf-8"))
            await ctx.send("insults reloaded")

def setup(bot):
    bot.add_cog(insultCommands(bot))
