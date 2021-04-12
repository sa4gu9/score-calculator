import math
import json
import os
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials


nick = []
score = []
winstrike = []
datas = ""
bonus = []

scoreminusratio = [1.00, 0.5, 0.3, 0.25, 0.2, 0.15, 0.15, 0.13, 0.12]

sup = []
sdown = []
who = []
rank = []
team = []
kill = []
tempscore = []
sumscore = []
temprank = []

fulldata = {}

retirebool = False
killMode = False

spreadbool = False
sumbool = False

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
sheetname = []
sheet = None


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
filename = input() + ".json"

print("직접 결과를 입력하려면 hand를, 구글 스프레드시트를 이용하려면 google을 입력해주세요.")
# inputtext = input()
inputtext = "google"

includekillscore = None

if inputtext == "hand":
    sheetamount = 1
    pass
elif inputtext == "google":
    spreadbool = True

    print("구글 스프레드시트 json파일 이름을 입력해주세요.")
    # json_file_name = input() + ".json"
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


else:
    exit()


if os.path.isfile(filename):
    with open(filename, "r", encoding="UTF-8") as jsonfile:
        fulldata = json.load(jsonfile)

people = 0
maxpeople = len(scoreminusratio) + 1

for sheetindex in range(sheetamount):
    time.sleep(30)
    nick.clear()
    score.clear()
    winstrike.clear()
    bonus.clear()
    sup.clear()
    sdown.clear()
    who.clear()
    rank.clear()
    team.clear()
    kill.clear()
    tempscore.clear()
    temprank.clear()

    if not spreadbool:
        while people < 2 or people > len(scoreminusratio):
            print(f"참가인원(2명~{maxpeople}명)을 입력하세요>>")
            people = int(input())

        print("경기 수를 입력해주세요>>")
        track = int(input())
    else:
        sheet = gc.open(spreadsheet_name).worksheet(sheetname[sheetindex])
        sheetvalue = sheet.get_all_values()
        people = int(sheetvalue[0][1])
        track = int(sheetvalue[0][3])

    for i in range(people):
        nickname = None
        if not spreadbool:
            print("참가 할 사람의 닉네임을 입력하세요>>")
            nickname = input()
            nick.append(nickname)
        else:
            nickname = sheetvalue[1][1 + i * 2]
            nick.append(nickname)

        if nickname in fulldata.keys():
            score.append(fulldata[nickname]["score"])
            winstrike.append(fulldata[nickname]["winstrike"])

        else:
            score.append(10)
            winstrike.append(0)
        rank.append(0)
        sdown.append(0)
        sup.append(0)
        bonus.append(0)
        kill.append(0)
        tempscore.append(0)
        temprank.append(0)
        sumscore.append(0)

    for i in range(track):

        retire = 0

        if retirebool:
            if not spreadbool:
                print("리타이어 수를 입력하세요>>")
                retire = int(input())

        for j in range(people):
            tempscore[j] = 0
            if not spreadbool:
                print(f"{nick[j]}의 등수는? 리타는 {maxpeople+1}로 입력>>")
                rank[j] = int(input())
                if rank[j] == maxpeople + 1:
                    rank[j] = people - retire + 1

            else:
                rank[j] = int(sheetvalue[3 + i][1 + j * 2])
                temprank[j] = rank[j]
                tempindex = 9 * (rank[j] - 1) + (people - 2)
                temps = int(includekillscore[tempindex].value)
                tempscore[j] += temps

            if killMode:
                if not spreadbool:
                    print(f"{nick[j]}의 킬 수는?")
                    kill[j] = int(input())
                else:
                    kill[j] = int(sheetvalue[3 + i][2 + j * 2])

                for kk in range(kill[j]):
                    if kk == 0:
                        tempscore[j] += 4
                    elif kk == 1:
                        tempscore[j] += 2
                    else:
                        tempscore[j] += 1

            sumscore[j] += tempscore[j]

        print(f"sumscore : {sumscore}")

        for j in range(people):
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
            a = 0.0
            b = 0.0
            win = 0
            lose = 0
            sup[j] = 0
            sdown[j] = 0
            myrank = 1
            for k in range(people):
                if rank[j] > rank[k]:
                    lose = lose + 1
                    a = a + score[k]
                elif rank[j] < rank[k]:
                    win = win + 1
                    b = b + score[k]

            if lose != 0:
                a = a / lose

            if win != 0:
                b = b / win

            if rank[j] == 1:
                winstrike[j] = winstrike[j] + 1
            else:
                winstrike[j] = 0

            if rank[j] != 1:
                if score[j] > a:
                    sdown[j] = 1 + 0.15 * math.floor(score[j] - a)
                else:
                    sdown[j] = 1 - 0.15 * math.floor(a - score[j])

            if win != 0:
                if score[j] > b:
                    sup[j] = 1 - 0.15 * math.floor(score[j] - b) * (
                        1 - lose * scoreminusratio[people - 2]
                    )
                else:
                    sup[j] = 1 + 0.15 * math.floor(b - score[j]) * (
                        1 - lose * scoreminusratio[people - 2]
                    )

        print(sup)
        print(sdown)
        print(i)

        for j in range(people):
            bonus[j] = 1.0
            if rank[j] == 1:
                if not winstrike == 1:
                    temp = winstrike[j]
                    while temp > 0:
                        bonus[j] = bonus[j] + 0.01 * temp
                        temp = temp - 1
                sup[j] = sup[j] * bonus[j]

            sdown[j] = sdown[j]

            if sdown[j] < 0:
                sdown[j] = 0

            if sup[j] < 0:
                sup[j] = 0

            score[j] = score[j] + sup[j]
            score[j] = score[j] - sdown[j]
            if score[j] < 0:
                score[j] = 0
            else:
                score[j] = round(score[j], 4)

    for i in range(people):
        fulldata[nick[i]] = {"score": score[i], "winstrike": winstrike[i]}
        print(f"{nick[i]} : {score[i]}P   {winstrike[i]}ws")

        if sumbool:
            print(sumscore[i])

if input("결과를 저장할려면 yes를 입력") == "yes":
    with open(filename, "w", encoding="UTF-8") as jsonfile:
        json.dump(fulldata, jsonfile, indent=4)
