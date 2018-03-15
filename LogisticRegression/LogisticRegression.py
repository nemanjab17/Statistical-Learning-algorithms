from pandas import read_json, DataFrame, read_csv, Series
import numpy as np
import math
from sklearn.utils import shuffle

df = read_csv('btc.csv')
df['volprev'] = np.log(df['volprev'])
df['lag1'] = df['lag1']*100
df['lag2'] = df['lag2']*100
df['lag3'] = df['lag3']*100
df['lag4'] = df['lag4']*100
df['lag5'] =df['lag5']*100
testset = df[366:466]
df = df[:365]



def gradient_descent(y, alpha, iterations, *args):
    #[0] - x1
    print("Running gradient descent..")
    y = DataFrame(y)
    thetas = np.zeros(len(args)+1)
    n = y.size
    for i in range(iterations):
        gofx= thetas[0]
        for j in range(0,len(args)):
            gofx += thetas[j+1]*args[j]
        hofx = Series([math.exp(value)/(1+math.exp(value)) for index,value in gofx.iteritems()])
        cost = (sum(y.y-gofx))/n
        gradientlist = []
        grad0 = (1/n)*sum(hofx-y.y)
        gradientlist.append(grad0)
        for j in range(1,len(thetas)):
            grad = (1/n)*sum((hofx-y.y)*args[j-1])
            gradientlist.append(grad)
        thetas[0] -= alpha*grad0
        for j in range(1, len(thetas)):
            thetas[j] -= alpha*gradientlist[j]
        #print last 10% of iterations, to see if it converges
        if i > iterations*0.9:
            print(cost)
    return thetas

def test_model(thetas, df):
    realvalue = df['y'].item()
    gofx = thetas[0]+thetas[1]*df['lag1']+thetas[2]*df['lag2']+thetas[3]*df['lag3']+thetas[4]*df['lag4']+thetas[5]*df['lag5']+thetas[6]*df['volprev']
    pred = math.exp(gofx)/(1+math.exp(gofx))
    if pred >= 0.5:
        predx = 1
    else:
        predx = 0
    return realvalue, predx

#run alg
thetas = gradient_descent(df['y'],0.0005, 2000, df['lag1'], df['lag2'], df['lag3'], df['lag4'], df['lag5'], df['volprev'])

#evaluate
dataset = 0
success = 0
for i in range(0,len(testset)-1):
    dataset += 1
    testdf = testset[i:i+1]
    realvalue, pred = test_model(thetas, testdf)
    dataset+=1
    if realvalue == pred:
        success +=1
output = "Success rate: " + str((success/dataset))
print(output)
print("sorry if i got you excited, but the result is very poor ;(")