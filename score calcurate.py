import math
import json
import os

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

fulldata = {}

retirebool = False
killbool = False

spreadbool = False

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
sheetname = None
sheet = None

print("데이터 이름을 입력하세요.")
filename = input() + ".json"

print("직접 결과를 입력하려면 hand를, 구글 스프레드시트를 이용하려면 google을 입력해주세요.")
inputtext = input()

includekillscore = None

if inputtext == "hand":
    pass
elif inputtext == "google":
    spreadbool = True

    print("구글 스프레드시트 json파일 이름을 입력해주세요.")
    json_file_name = input() + ".json"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file_name, scope
    )

    gc = gspread.authorize(credentials)

    print("구글 스프레드시트 이름을 입력해주세요.")
    spreadsheet_name = input()

    print("시트이름을 입력해주세요.")
    sheetname = input()

    sheet = gc.open(spreadsheet_name).worksheet(sheetname)

    scoresheet = gc.open(spreadsheet_name).worksheet("킬점수반영시 점수표")
    includekillscore = scoresheet.range("B2:J11")

    print(includekillscore)


else:
    exit()


if os.path.isfile(filename):
    with open(filename, "r", encoding="UTF-8") as jsonfile:
        fulldata = json.load(jsonfile)

people = 0
maxpeople = len(scoreminusratio) + 1

if not spreadbool:
    while people < 2 or people > len(scoreminusratio):
        print(f"참가인원(2명~{maxpeople}명)을 입력하세요>>")
        people = int(input())

    print("경기 수를 입력해주세요>>")
    track = int(input())
else:
    people = int(sheet.cell(1, 2).value)
    track = int(sheet.cell(1, 4).value)

print("공동 최하위(리타이어)가 필요하다면 retire를 입력해주세요.")
inputdata = input()
if inputdata == "retire":
    retirebool = True
    print("리타이어 모드를 적용합니다.")
    retire = 0

print("킬포함 점수를 측정하고 싶다면 kill을 입력해주세요.")
inputdata = input()
if inputdata == "kill":
    killbool = True
    print("킬 모드를 적용합니다.")

for i in range(people):
    nickname = None
    if not spreadbool:
        print("참가 할 사람의 닉네임을 입력하세요>>")
        nickname = input()
        nick.append(nickname)
    else:
        nick.append(sheet.cell(2, 2 + i * 2).value)

    if nickname in fulldata.keys():
        score.append(fulldata[nickname]["score"])
        winstrike.append(fulldata[nickname]["winstrike"])
        print(fulldata[nickname])
    else:
        score.append(10)
        winstrike.append(0)
    rank.append(0)
    sdown.append(0)
    sup.append(0)
    bonus.append(0)
    kill.append(0)


for i in range(track):
    if retirebool:
        print("리타이어 수를 입력하세요>>")
        retire = int(input())
    rowvalues = None

    if spreadbool:
        rowvalues = sheet.row_values(4 + i)
    print(rowvalues)

    for j in range(people):
        if not spreadbool:
            print(f"{nick[j]}의 등수는? 리타는 {maxpeople+1}로 입력>>")
            rank[j] = int(input())
            if rank[j] == maxpeople + 1:
                rank[j] = people - retire + 1
        else:
            print([i, j])
            rank[j] = int(rowvalues[1 + 2 * j])

        if killbool:
            if not spreadbool:
                print(f"{nick[j]}의 킬 수는?")
                kill[j] = int(input())
            else:
                kill[j] = int(rowvalues[2 + 2 * j])

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
        score[j] = score[j] + sup[j]
        score[j] = score[j] - sdown[j]
        if score[j] < 0:
            score[j] = 0
        else:
            score[j] = round(score[j], 4)

for i in range(people):
    fulldata[nick[i]] = {"score": score[i], "winstrike": winstrike[i]}
    print(f"{nick[i]} : {score[i]}P   {winstrike[i]}ws")


with open(filename, "w", encoding="UTF-8") as jsonfile:
    json.dump(fulldata, jsonfile, indent=4)
