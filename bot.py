import json
from discord.ext import commands
import discord
import os
import ScoreCalcurate


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
        await ctx.send(returnData)
        return
    rankData = ScoreCalcurate.GetAllData(dataname)
    for data in rankData:
        if data[0] == username:
            await ctx.send(f"{data[0]} {data[1]} {rankData.index(data)+1}")
            return
    await ctx.send("존재하지 않는 유저입니다.")


bot.run(token["token"])