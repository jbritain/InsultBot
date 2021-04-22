from discord.ext import commands
import discord
import csv
import random

class insultCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.insults = []
        with open("src/insults.csv", "r") as insultList:
            insultReader = csv.reader(insultList, delimiter=',')
            for row in insultReader:
                for column in row:
                    self.insults.append(column)
        


    @commands.command(brief="Insult someone", description="Insult someone in the format `?insult @user-to-insult`")
    async def insult(self, ctx, person):
        if person == "@everyone":
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", "everyone"))
        elif person.replace("!", "") == self.bot.user.mention:
            await ctx.send(random.choice(self.insults).replace("?1", ctx.author.mention).replace("?2", self.bot.user.mention))
        else:
            await ctx.send(random.choice(self.insults).replace("?1", person).replace("?2", ctx.author.mention))

def setup(bot):
    bot.add_cog(insultCommands(bot))
