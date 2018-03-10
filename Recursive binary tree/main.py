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
#ideja je da imam neki dataset sa 2 kolone koje su prediktori i jednom koja je rezultat
#izvristi klasifikaciju tako sto se odrede klasteri na osnovu prediktora
#klasteri su kocke koje imaju najmanje 5 elemenata cija je suma kvadrata (yi-mean klastera)^2 za svako i minimalna
#to znaci da su kocke formirane i za odredjene vrednosti prediktora, svrstava se u kocku
#svaka kocka ima svoju y vrednost koja je u stvari predikcija

#autput:
#dimenzije kocke, tj x1,x2, y1,y2 i vrednost koja se procenjuje za tu kocku

#input:
#dataset:
#kolona1 = 1. prediktor
#kolona2 = 2. prediktor
#kolona3 = vrednosti
#naci max vrednosti, one odredjuju gornje granice, te prvu kocku
#u funkciju ubacujem gornje granice(kocka), donje granice i dataset
fields= []
def bst(newdf, x1, x2, y1, y2):
    global fields   
    # if len(newdf) < 10:
    #     #print((x1, x2, y1, y2))
    #     fields.append((x1, x2, y1, y2))
    #     return 0
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
    
    


def getvalue(newdf,fields,hits, years, actualsalary):
    for field in fields:
        if hits > field[0] and hits<=field[1] and years > field[2] and years<=field[3]:
            salarieslist = []
            for index,row in newdf.iterrows():
                if row['Hits'] > field[0] and row['Hits']<=field[1] and row['Years'] > field[2] and row['Years']<=field[3]:
                    salarieslist.append(row['Salary'])

    return np.power((salarieslist),2)

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



#result at 15 treshold
#fields = [(0, 3.29, 0, 3.1780538303479458), (3.29, 3.61, 0, 3.1780538303479458), (3.61, 3.8200000000000003, 0, 3.1780538303479458), (3.8200000000000003, 3.93, 0, 3.1780538303479458), (3.93, 4.0, 0, 3.1780538303479458), (4.0, 4.09, 0, 3.1780538303479458), (4.09, 4.18, 0, 3.1780538303479458), (4.18, 4.24, 0, 3.1780538303479458), (4.24, 4.3, 0, 3.1780538303479458), (4.3, 4.38, 0, 3.1780538303479458), (4.38, 4.43, 0, 3.1780538303479458), (4.43, 4.46, 0, 3.1780538303479458), (4.46, 4.54, 0, 3.1780538303479458), (4.54, 4.59, 0, 3.1780538303479458), (4.59, 4.68, 0, 3.1780538303479458), (4.68, 4.71, 0, 3.1780538303479458), (4.71, 4.7700000000000005, 0, 3.1780538303479458), (4.7700000000000005, 4.82, 0, 3.1780538303479458), (4.82, 4.87, 0, 3.1780538303479458), (4.87, 4.92, 0, 3.1780538303479458), (4.92, 4.95, 0, 3.1780538303479458), (4.95, 4.98, 0, 3.1780538303479458), (4.98, 5.03, 0, 3.1780538303479458), (5.03, 5.09, 0, 3.1780538303479458),(5.09, 5.11, 0, 3.1780538303479458), (5.11, 5.15, 0, 3.1780538303479458), (5.15, 5.28, 0, 3.1780538303479458), (5.28, 5.472270673671475, 0, 3.1780538303479458)]
#field = (0, 36, 0, 4)
#fields=[(36, 70, 0, 4),(70, 114, 0, 2),(70, 114, 2, 4),(114, 238, 0, 4),(0, 75, 4, 6),(75, 122, 4, 6),(0, 41, 6, 24),(41, 72, 6, 7),(41, 72, 7, 12),(41, 72, 12, 23),(41, 72, 23, 24),(72, 122, 6, 6)]


# odrediti linije koje ce podeili kocku
#tako sto cemo birati prediktor i vrednost koje minimiziraju sumu kvadrata
#kad se podeli na dva dela, onda se na oba dela ponovo poziva funkcija rekurzivno
#pa ce svaki deo ponovo da se podeli na dva dela,
#to se ponavlja dok nema 5-10 podataka u tom kvadratu, kad se to desi, sacuvati granice u nekoj
#listi van funkcije kao four-tuple(x1,x2,y1,y2)
#[(0, 3.29, 0, 3.1780538303479458), 
#(3.29, 4.09, 0, 3.1780538303479458), 
#(4.09, 4.46, 0, 3.1780538303479458), 
#(4.46, 4.87, 0, 3.1780538303479458), 
#(4.87, 5.09, 0, 3.1780538303479458), 
#(5.09, 5.472270673671475, 0, 3.1780538303479458)]