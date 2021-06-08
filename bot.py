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
async def 정보(ctx, dataname=None, sort=None, username=None):
    if dataname == None:
        datalist = os.listdir("data")
        senddata = ""
        for data in datalist:
            senddata += f"{data}\n"
        await ctx.send(senddata)
        return

    if username == None:
        printData = ScoreCalcurate.GetAllData(dataname, sort)

        totalLen = 0
        returnData = "```"
        for data in printData:
            totalLen += 1

            tempData = f"""{'%-2s'%totalLen} {'%-15s' % data[0]} {'%-9s' % data[1]}  {'%-9s' % data[2]}  {'%-5s' % data[3]}  {'%-2s' % data[4]}\n"""
            returnData += tempData

            if totalLen % 20 == 0:
                returnData += "```"
                await ctx.send(returnData)
                returnData = "```"

        returnData += "```"
        await ctx.send(returnData)
        return
    rankData = ScoreCalcurate.GetAllData(dataname, sort)

    for data in rankData:
        if data[0] == username:
            await ctx.send(
                f"""{'%-15s' % data[0]} {'%-9s' % data[1]}  {'%-9s' % data[2]}  {'%-5s' % data[3]}  {'%-2s' % rankData.index(data) + 1}위\n"""
            )

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
