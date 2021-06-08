import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


avgrank_list = []
score = []

jsonfile = open("data/ksdfromdl1.json", "r")
fulldata = json.load(jsonfile)
jsonfile.close()


for data in fulldata:
    userdata = fulldata[data]
    print(userdata)
    score.append(userdata["score"])
    totalgame = userdata["totalgame"]
    totalrank = userdata["totalrank"]
    sumMaxrank = userdata["sumMaxrank"]

    a = totalrank / totalgame - 1
    b = sumMaxrank / totalgame - 1

    avgrank_list.append(a / b * 100)


line_filter = LinearRegression()
templist = []
for i in avgrank_list:
    templist.append([i])
line_filter.fit(templist, score)
print(line_filter.predict([[100], [74], [50], [30], [10], [1]]))

plt.plot(avgrank_list, score, "o")
plt.gca().invert_xaxis()
plt.plot(avgrank_list, line_filter.predict(templist))
plt.show()
