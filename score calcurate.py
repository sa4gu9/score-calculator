import math
import json
import os

nick = []
score = []
winstrike = []
datas = ""
bonus = []

scoreminusratio = [1.00, 0.5, 0.3, 0.25, 0.2, 0.15, 0.15]

sup = []
sdown = []
who = []
rank = []
team = []

fulldata = {}

print("데이터 이름을 입력하세요.")
filename = input() + ".json"

if os.path.isfile(filename):
    with open(filename, "r", encoding="UTF-8") as jsonfile:
        fulldata = json.load(jsonfile)

print("참가인원을 입력하세요>>")
people = int(input())
for i in range(people):
    print("참가 할 사람의 닉네임을 입력하세요>>")
    nickname = input()
    nick.append(nickname)

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

print("경기 수를 입력해주세요>>")
track = int(input())

for i in range(track):
    print("리타이어 수를 입력하세요>>")
    retire = int(input())
    for j in range(people):
        print(f"{nick[j]}의 등수는? 리타는 9로 입력>>")
        rank[j] = int(input())
        if rank[j] == 9:
            rank[j] = people - retire + 1

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
                sup[j] = 1 - 0.15 * math.floor(score[j] - b)
            else:
                sup[j] = 1 + 0.15 * math.floor(b - score[j])

    for j in range(people):
        bonus[j] = 1.0
        if rank[j] == 1:
            if not winstrike == 1:
                temp = winstrike[j]
                while temp > 0:
                    bonus[j] = bonus[j] + 0.01 * temp
                    temp = temp - 1
            sup[j] = sup[j] * bonus[j]

        sdown[j] = sdown[j] * (1 - lose * scoreminusratio[people - 2])
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
    json.dump(fulldata, jsonfile)
