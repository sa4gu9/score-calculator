import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


def CheckDigit(temp):
    try:
        tmp = float(temp)
        return True
    except ValueError:
        return False


dir = "leaguedata/singles/2020 시즌2"
datalist = os.listdir(dir)

json_file_name = "spreadjson.json"


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_name = "2020카트 시즌2"

fileindex = 0

for filename in datalist:

    file = open(dir + "/" + filename, mode="r", encoding="UTF-8")

    data1 = file.readlines()
    file.close()

    for line in data1:
        print(line)

    print("시트이름을 입력해주세요.")
    sheetname = input()
    sheet = gc.open(spreadsheet_name).worksheet(sheetname)

    index = -1

    for line in data1:

        writedata = []

        line = line.split("\t")

        if index == -1:
            i = 0
            for temp in line:
                if i < 8:
                    print(i, temp)
                    sheet.update_cell(2, 3 + i * 2, temp)
                    i += 1
        else:
            temprank = []

            print(line)
            for tempscore in line:
                if CheckDigit(tempscore):
                    temprank.append(int(tempscore))
                else:
                    print(tempscore)
                    temprank.insert(0, tempscore.replace("\n", ""))
            print(temprank)

            for temp in temprank:
                crank = 1
                cindex = 1
                if CheckDigit(temp):
                    for i in range(len(temprank) - 1):
                        if temp < temprank[i + 1]:
                            crank += 1
                        else:
                            pass
                    writedata[0].extend([crank, ""])
                else:
                    writedata.append([temp])

            print(writedata)
            sheet.update(f"B{4+index}:R{4+index}", writedata)

        index += 1

    time.sleep(15)
    os.remove(dir + "/" + filename)
