from discord.ext import commands
import discord
import random
import urllib

class insultCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.insults = []
        data = urllib.request.urlopen("https://pr0x1mas.github.io/InsultBot/src/insults.csv")
        for line in data:
            self.insults.append(line.decode("utf-8"))
            print(line.decode("utf-8"))
        


    @commands.command(brief="Insult someone", description="Insult someone in the format `?insult @user-to-insult`")
    async def insult(self, ctx, person):
        if person == "@everyone":
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", "everyone"))
        elif person.replace("!", "") == self.bot.user.mention:
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", self.bot.user.mention))
        else:
            await ctx.send(random.choice(self.insults).replace("?1", person).replace("?2", ctx.author.mention))

    @commands.command()
    async def reload(self, ctx):
        await ctx.send("reloading insults...")
        async with ctx.typing():
            self.insults = []
            data = urllib.request.urlopen("https://pr0x1mas.github.io/InsultBot/src/insults.csv")
            for line in data:
                self.insults.append(line.decode("utf-8"))
            await ctx.send("insults reloaded")

def setup(bot):
    bot.add_cog(insultCommands(bot))
