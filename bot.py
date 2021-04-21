import json
from discord.ext import commands
import discord
import ScoreCalcurate

tokenfile = open("token.json", "r")
bot = commands.Bot(command_prefix=">")
token = json.load(tokenfile)


@bot.command()
async def 모두보기(ctx, dataname):
    printData = ScoreCalcurate.GetAllData(dataname)
    await ctx.send(printData)
    return


bot.run(token["token"])