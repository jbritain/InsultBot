from discord.ext import commands
import discord
import random
import urllib

class insultCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.insults = []
        data = urllib.request.urlopen("https://raw.githack.com/Pr0x1mas/InsultBot/main/src/insults.csv") # get insults from online list
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

    @commands.command(brief="Reload all insults", description="Reload all insults, only accessable by bot owner")
    @commands.is_owner()
    async def reload(self, ctx): # reload all insults
        await ctx.send("reloading insults...")
        async with ctx.typing():
            self.insults = []
            data = urllib.request.urlopen("https://raw.githack.com/Pr0x1mas/InsultBot/main/src/insults.csv") # get insults from online list
            i = 0
            for line in data:
                self.insults.append(line.decode("utf-8"))
                print("loaded insult " + line.decode("utf-8"))
                i += 1
            await ctx.send(str(i) + " insults loaded")

    @commands.command(brief="Submit an insult", description="Submit an insult you think should be added to the list of insults used by the bot")
    async def submit(self, ctx, insult, extraargs=None):
        if extraargs is None:
            with open("submissions.txt", "a") as submissionList:
                submissionList.write(insult + "\n")
                await ctx.send("Insult submitted!")
        else:
            await ctx.send("Insult submissions must be contained in quote marks \"like this\"")


def setup(bot):
    bot.add_cog(insultCommands(bot))
