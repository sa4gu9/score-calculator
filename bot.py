import json
from discord.ext import commands
import discord
import os
import ScoreCalcurate
from datetime import datetime
import betting


tokenfile = open("token.json", "r")
bot = commands.Bot(command_prefix=">")
token = json.load(tokenfile)


@bot.command()
async def 정보(ctx, dataname=None, username=None):
    if dataname == None:
        datalist = os.listdir("data")
        senddata = ""
        for data in datalist:
            senddata += f"{data}\n"
        await ctx.send(senddata)
        return

    if username == None:
        printData = ScoreCalcurate.GetAllData(dataname)
        returnData = ""
        for data in printData:
            tempData = f"{data[0]} : {data[1]}\n"
            returnData += tempData
        await ctx.author.send(returnData)
        return
    rankData = ScoreCalcurate.GetAllData(dataname)
    for data in rankData:
        if data[0] == username:
            await ctx.send(f"{data[0]} {data[1]} {rankData.index(data)+1}")
            return
    await ctx.send("존재하지 않는 유저입니다.")


@bot.command()
async def 베팅(ctx, betname=None, index=None, betmoa=None):
    betinfo = betting.GetBetinfo(betname)

    if betname == None:
        for info in betinfo:
            await ctx.send(info)
    else:
        await ctx.send(betinfo)
    # now = datetime.now()
    # today = f"{now.year}{now.month}{now.day}"


bot.run(token["token"])
