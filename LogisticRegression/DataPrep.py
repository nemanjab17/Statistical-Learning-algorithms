from pandas import read_json, DataFrame
import requests
from bs4 import BeautifulSoup

r = requests.get('https://apiv2.bitcoinaverage.com/indices/global/history/BTCUSD?period=alltime&format=json')
jsre = r.json()
df = DataFrame.from_dict(jsre)
df1 = df['average']
returnvalues = [0]
for i in range(0, len(df)-1):
    returnvalues.append(round((df1.loc[i+1]-df1.loc[i])/df1.loc[i],4))
newdf = DataFrame(returnvalues, columns=['return'])
newdf = newdf[1:]
df = df[1:]
df = df.merge(newdf, right_index=True, left_index=True, how='inner')
newdflist = []
for i in range(5,len(df)):
    newdflist.append((df.iloc[i,6],df.iloc[i-1,6],df.iloc[i-2,6],df.iloc[i-3,6],df.iloc[i-4,6],df.iloc[i-5,6], df.iloc[i-1,5], df.iloc[i,4]))
newdf = DataFrame(newdflist, columns=['y', 'lag1','lag2','lag3','lag4','lag5','volprev', 'date'])
newlist =[]
for index,row in newdf.iterrows():
    if row['y'] >= 0.0:
        newlist.append(1)
    else:
        newlist.append(0)
newdf['y'] = Series(newlist)
newdf.to_csv('btc.csv', sep=',')
print(newdf.head(20))
        