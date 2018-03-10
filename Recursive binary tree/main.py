from pandas import DataFrame, Series, read_csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

xlsx = read_csv('data.csv')
newdf = DataFrame(xlsx[['Hits', 'Years', 'Salary']])
newdf = newdf[newdf['Salary'].notna()]
newdf['Salary'] = newdf['Salary'].apply(np.log)
maxhits = newdf['Hits'].max()
maxyears = newdf['Years'].max()
firstbox = (maxhits, maxyears)

fields= []
def bst(newdf, x1, x2, y1, y2):
    global fields   
    currentrss = 100000000
    currents = 0
    currentp= 0
    #predictor 0 = hits, predicotr 1 = years
    predictors = [0, 1]
    for i in predictors:
        if i == 0:
            predhigh = x2
            predrow = 'Hits'
        else:
            predhigh = y2
            predrow = 'Years'
        for s in range(predhigh):
            higherlist = []
            lowerlist = []
            for index, row in newdf.iterrows():
                if row[predrow] <= s:
                    lowerlist.append(row['Salary'])
                else:
                    higherlist.append(row['Salary'])
            meanlower = np.mean(lowerlist)
            meanhigher = np.mean(higherlist)
            lowersum = 0
            highersum = 0
            for k in lowerlist:
                lowersum += np.power((k-meanlower),2)
            for r in higherlist:
                highersum += np.power((r-meanhigher),2)
            newrss = lowersum + highersum
            if newrss <= currentrss and lowerlist > 5 and higherlist > 5:
                currentrss = newrss
                currents = s
                currentp = i
    if currentp == 0:
        row_to_evaluate = 'Hits'
    else:
        row_to_evaluate = 'Years'

    lowerindex= []
    higherindex= []
    for index, row in newdf.iterrows():
        if row[row_to_evaluate] < currents:
            lowerindex.append(index)
        else:
            higherindex.append(index)
    lowerdf = newdf[newdf.index.isin(lowerindex)]
    higherdf = newdf[newdf.index.isin(higherindex)]
    if len(lowerdf) < 5  or len(higherdf) <5:
        fields.append((x1, x2, y1, y2))
        print(len(lowerdf), len(higherdf))
        return 0
    if currentp == 0:
        x = bst(lowerdf,x1, currents, y1, y2)
        x = bst(higherdf,currents, x2, y1, y2)
    else:
        x = bst(lowerdf, x1, x2, y1, currents)
        x = bst(higherdf,x1, x2, currents, y2)
    return 0

x = bst(newdf,0, maxhits,0,maxyears)
fig, ax = plt.subplots()
x = newdf['Hits']
y = newdf['Years']
ax.scatter(x, y, marker='.')
for i in fields:
    ax.add_patch(patches.Rectangle(
        (i[0], i[2]),
        i[1]-i[0],
        i[3]-i[2],
        fill=False      # remove background
    ))
plt.show()

