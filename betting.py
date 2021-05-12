import json


def RegisterBet():
    return


def GetBetinfo(betname=None):
    f = open("todaybet.json", "r")
    todaybet = json.load(f)
    f.close()
    modes = ""

    if betname == None:
        betlist = []
        for bet in todaybet.keys():
            for info in todaybet[bet].keys():
                if info == "mode":
                    if todaybet[bet][info] == "sum":
                        modes = f"오늘 {todaybet[bet]['rank']}위"
                    # elif todaybet[bet][info] == "score":
                    #     modes = f"랭크 점수 {todaybet[bet]['rank']}위"

            betlist.append(
                f"""{bet} : {todaybet[bet]["date"]} {todaybet[bet]['game']}이후 {modes}"""
            )
        return betlist
    else:
        if betname in todaybet.keys():
            betinfo = todaybet[betname]
            if betinfo["mode"] == "sum":
                modes = f"오늘 {todaybet['rank']}위"
            # elif betinfo["mode"] == "score":
            #     modes = f"랭크 점수 {betinfo['rank']}위"
            return f"{betinfo['date']} {betinfo['game']}이후 {modes}"
        else:
            return "찾을 수 없습니다"