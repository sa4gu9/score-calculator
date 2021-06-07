import math
import json
import os
import time
import elo

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pandas.core.base import NoNewAttributesMixin

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
sheetname = []
sheet = None


def GetSheetValue(gc, spreadsheet_name, sheetname):
    sheet = gc.open(spreadsheet_name).worksheet(sheetname)
    sheetvalue = sheet.get_all_values()
    return sheetvalue


def GetAllData(filename, sort):
    ranklist = []
    with open("data/" + filename, "r", encoding="UTF-8") as f:
        alldata = json.load(f)
    for user in alldata.keys():
        avgmax = round(alldata[user]["sumMaxrank"] / alldata[user]["totalgame"], 2)
        avgrank = round(alldata[user]["totalrank"] / alldata[user]["totalgame"], 2)
        rankpercent = round((avgrank - 1) / (avgmax - 1) * 100, 2)
        calpercent = 1 - rankpercent * 0.01

        totalscore = round(alldata[user]["score"] * calpercent, 4)

        rank = 0
        for data in ranklist:
            if sort == "score":
                if data[1] > alldata[user]["score"]:
                    rank += 1
            elif sort == "avgrank":
                if data[3] < rankpercent:
                    rank += 1

        ranklist.insert(
            rank,
            [
                user,
                alldata[user]["score"],
                f"{avgrank}/{avgmax}",
                rankpercent,
            ],
        )
    return ranklist


def InputFilename():
    print("파일 이름 입력")
    filename = "data/" + input() + ".json"

    return filename


fulldata = {}


def RunProgram():
    global fulldata

    nick = []
    score = []
    winstrike = []
    bonus = []

    scoreminusratio = [1.00, 0.5, 0.3, 0.25, 0.2, 0.15, 0.15, 0.13, 0.12]

    who = []
    rank = []
    team = []
    kill = []
    tempscore = []
    sumscore = []
    temprank = []

    totalrank = []
    sumMaxrank = []
    totalgame = []

    killMode = False

    sumbool = False

    print("점수와 순위를 보고싶으면 rank 입력")
    if input() == "rank":
        filename = InputFilename()
        GetAllData(filename)
        exit()

    print("킬포함 점수를 측정하고 싶다면 kill을 입력해주세요.")
    inputdata = input()

    if inputdata == "kill":
        killMode = True
        print("킬 모드를 적용합니다.")

    inputdata = input("누적모드를 적용하려면 sum을 입력해주세요.")
    if inputdata == "sum":
        sumbool = True
        print("누적모드를 적용합니다.")

    print("데이터 이름을 입력하세요.")
    filename = "data/" + input() + ".json"

    includekillscore = None

    json_file_name = "spreadjson.json"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file_name, scope
    )

    gc = gspread.authorize(credentials)

    print("구글 스프레드시트 이름을 입력해주세요.")
    spreadsheet_name = input()

    if sumbool:
        sheetamount = 1
    else:
        print("시트 개수를 입력하세요.")
        sheetamount = int(input())

    for aa in range(sheetamount):
        print("시트이름을 입력해주세요.")
        sheetname.append(input())

    scoresheet = gc.open(spreadsheet_name).worksheet("킬점수반영시 점수표")
    includekillscore = scoresheet.range("B2:J11")

    if os.path.isfile(filename):
        with open(filename, "r", encoding="UTF-8") as jsonfile:
            fulldata = json.load(jsonfile)

    people = 0
    maxpeople = len(scoreminusratio) + 1

    for sheetindex in range(sheetamount):
        time.sleep(3)

        nick.clear()
        score.clear()
        winstrike.clear()
        bonus.clear()
        who.clear()
        rank.clear()
        team.clear()
        kill.clear()
        tempscore.clear()
        temprank.clear()
        sumscore.clear()

        totalrank.clear()
        sumMaxrank.clear()
        totalgame.clear()

        sheetvalue = GetSheetValue(gc, spreadsheet_name, sheetname[sheetindex])

        people = int(sheetvalue[0][1])
        track = int(sheetvalue[0][3])

        for i in range(people):

            nickname = sheetvalue[1][2 + i * 2]
            nick.append(nickname)

            if nickname in fulldata.keys():
                score.append(fulldata[nickname]["score"])
                winstrike.append(fulldata[nickname]["winstrike"])

                totalrank.append(fulldata[nickname]["totalrank"])
                sumMaxrank.append(fulldata[nickname]["sumMaxrank"])
                totalgame.append(fulldata[nickname]["totalgame"])

            else:
                fulldata[nickname] = {
                    "score": 2000,
                    "winstrike": 0,
                    "totalrank": 0,
                    "sumMaxrank": 0,
                    "totalgame": 0,
                }

            rank.append(0)
            bonus.append(0)
            kill.append(0)
            tempscore.append(0)
            temprank.append(0)
            sumscore.append(0)

        for i in range(track):
            tempPeople = 0
            retire = 0

            for j in range(people):
                tempscore[j] = 0

                mapname = sheetvalue[3 + i][1]
                checkrank = sheetvalue[3 + i][2 + j * 2]
                if not checkrank == "X":
                    tempPeople += 1
                    rank[j] = int(checkrank)
                    temprank[j] = rank[j]
                    tempindex = 9 * (rank[j] - 1) + (people - 2)
                    temps = int(includekillscore[tempindex].value)
                    tempscore[j] += temps
                else:
                    rank[j] = "not check"

                if killMode:
                    if rank[j] == "not check":
                        continue
                    else:
                        kill[j] = int(sheetvalue[3 + i][2 + j * 2])

                    for kk in range(kill[j]):
                        if kk == 0:
                            tempscore[j] += sheetvalue[27][3]
                        elif kk == 1:
                            tempscore[j] += sheetvalue[27][4]
                        else:
                            tempscore[j] += sheetvalue[27][5]

                sumscore[j] += tempscore[j]

            for j in range(people):
                if rank[j] == "not check":
                    continue
                index = -1
                rank[j] = 1

                for ss in tempscore:
                    index += 1
                    if index == j:
                        continue
                    if tempscore[j] < ss:
                        rank[j] += 1
                    elif tempscore[j] == ss:
                        if temprank[j] > temprank[index]:
                            rank[j] += 1

            print(rank)

            for j in range(people):
                if rank[j] == "not check":
                    continue

                loseScore = 0.0
                winScore = 0.0
                win = 0
                lose = 0

                for k in range(people):
                    if rank[k] == "not check":
                        continue
                    if rank[j] > rank[k]:
                        lose = lose + 1
                        loseScore += fulldata[nick[k]]["score"]
                    elif rank[j] < rank[k]:
                        win = win + 1
                        winScore += fulldata[nick[k]]["score"]

                if lose != 0:
                    loseScore = loseScore / lose

                if win != 0:
                    winScore = winScore / win

                if rank[j] == 1:
                    fulldata[nick[j]]["winstrike"] += 1
                else:
                    fulldata[nick[j]]["winstrike"] = 0

                downpercent = 0

                if rank[j] == 1:
                    downpercent = 0
                else:
                    if not rank[j] == GetMax(rank):
                        if people > 10:
                            if rank[j] > 10:
                                downpercent = 1
                            else:
                                downpercent = lose * scoreminusratio[9]
                        else:
                            downpercent = lose * scoreminusratio[people - 2]
                    else:
                        downpercent = 1

                uppercent = 1

                if rank[j] == 1:
                    temp = fulldata[nick[j]]["winstrike"]
                    strikeBonus = 0
                    if not temp == 1:
                        while temp > 0:
                            strikeBonus += 0.05 * temp
                            temp = temp - 1

                    if tempPeople > 3:
                        uppercent = 1 + strikeBonus * (tempPeople - 3)

                changeScore = GetChangeScore(
                    fulldata[nick[j]]["score"],
                    winScore,
                    loseScore,
                    uppercent,
                    downpercent,
                )

                fulldata[nick[j]]["totalrank"] += rank[j]
                fulldata[nick[j]]["sumMaxrank"] += tempPeople
                fulldata[nick[j]]["totalgame"] += 1
                fulldata[nick[j]]["score"] = round(
                    fulldata[nick[j]]["score"] + changeScore, 4
                )

        for i in range(people):
            userdata = fulldata[nick[i]]
            avgmax = userdata["sumMaxrank"] / userdata["totalgame"]
            avgrank = userdata["totalrank"] / userdata["totalgame"]

            print(
                f"{nick[i]} : {userdata['score']}P   {userdata['winstrike']}ws {avgrank}/{avgmax}"
            )

            if sumbool:
                print(sumscore[i])

    SaveData(filename, fulldata)


def SaveData(filename, fulldata):
    if input("결과를 저장할려면 yes를 입력") == "yes":
        with open(filename, "w", encoding="UTF-8") as jsonfile:
            json.dump(fulldata, jsonfile, indent=4)


def GetMax(rank):
    returnValue = None
    for i in rank:
        if i == "not check":
            continue
        else:
            if returnValue == None:
                returnValue = i
            else:
                if i > returnValue:
                    returnValue = i
    return returnValue


def GetChangeScore(myScore, winScore, loseScore, uppercent, downpercent):

    sup = abs(myScore - elo.rate_1vs1(myScore, winScore)[0]) * uppercent

    sdown = abs(myScore - elo.rate_1vs1(loseScore, myScore)[1]) * downpercent

    return sup - sdown
