import csv, math, random, json
import DPlib, PNlib

import numpy as np
import pylab as P

#name = 'CCMHOCKEY'
#name = 'CARTERS'
#name = 'SYNCFROG'
#name = '99DESIGNS'
#name = 'BAUERHOCKEY'
#name = 'HIREVUE'
#name = 'ADVANCEAUTO'
#name = 'GETRESPONSE'
name = 'SALESLOFT'
#name = 'SALESWISE'

dBG = DPlib.getBG()

dKT, lKT, sdKT, aKT = DPlib.getKT(name)

dDIFF, sdDIFF = DPlib.getDIFF(dBG, dKT, sdKT)

X, Y = PNlib.plotTOPICS(name, sdDIFF, dKT)

TOP = DPlib.getTOP(X, Y, sdDIFF)

AM, lAM = DPlib.generateAM(TOP, lKT)

DPlib.generateDATA(name, TOP, dDIFF, dKT, aKT, lAM, AM)

"""
def getKT(name):
    f = open('DATA/'+name+'.csv')

    reader = csv.reader(f)

    KT = []
    lKT = []
    for row in reader:
        #print row[25].replace('[','').replace(']','').replace('"','').replace(' ','').split(',')
        KT = KT + row[25].replace('[','').replace(']','').replace('"','').replace(' ','').split(',')
        lKT.append(row[25].replace('[','').replace(']','').replace('"','').replace(' ','').split(','))

    TOT = len(KT)
    dKT = {x:-math.log(1.*KT.count(x)/TOT) for x in list(set(KT))}


    sdKT =  sorted(dKT.items(), key=lambda x: x[1])

    return dKT, lKT, sdKT

def getDIFF(dBG, dKT, sdKT):

    dDIFF = {}

    for key in sdKT:
        try:
            com = dKT[key[0]]
            bg = dBG[key[0]]
 
            #print key[0], dKT[key[0]], dBG[key[0]]

            dDIFF[key[0]] = (dKT[key[0]] - dBG[key[0]])/dBG[key[0]]
        except:
            pass
        
            
    sdDIFF =  sorted(dDIFF.items(), key=lambda x: x[1])
    return dDIFF, sdDIFF










def plotTOPICS(sdDIFF, dKT):

    vCOMM =[]
    vDIFF = []

    for i in range(len(sdDIFF)):
        #print sdDIFF[i][0], -sdDIFF[i][1], dKT[sdDIFF[i][0]]
        vDIFF.append(-sdDIFF[i][1])
        vCOMM.append(dKT[sdDIFF[i][0]])

    nDIFF = np.array(vDIFF)
    nCOMM = np.array(vCOMM)
    
    mDIFF = np.mean(nDIFF)
    sDIFF = np.std(nDIFF)

    mCOMM =np.mean(nCOMM)
    sCOMM =np.std(nCOMM)


    X = []
    Y = []
    for j in range(len(sdDIFF)):
        x = (max(nCOMM) - nCOMM[j])/(max(nCOMM) - min(nCOMM))
        y = (nDIFF[j] - min(nDIFF))/(max(nDIFF) - min(nDIFF))

        X.append(x)

        Y.append(y)

    P.scatter(X, Y)
    P.show()

    return X, Y

def getTOP(X, Y, sdDIFF):

    nX = np.array(X)
    nY = np.array(Y)

    mX = np.mean(nX)
    sX = np.std(nX)

    mY = np.mean(nY)
    sY = np.std(nY)

    TOP = {}
    count = 0

    for ii in range(len(nX)):
        if nX[ii] > mX + sX and nY[ii] > mY + sY:
            TOP[sdDIFF[ii][0]] = count 
            count = count + 1

    return TOP

def generateAM(TOP, lKT):

    AM = [[1 for i in range(len(TOP))] for j in range(len(TOP))]

    for item in lKT:
        IDX = []
    
        if len(item)>0:
            for instance in item:
                if instance in TOP.keys():
                    IDX.append(TOP[instance])
        
        if len(IDX)>1:
            for i in range(len(IDX)):
                for j in range(i):
                    AM[IDX[i]][IDX[j]] = AM[IDX[i]][IDX[j]] + 1
                    AM[IDX[j]][IDX[i]] = AM[IDX[j]][IDX[i]] + 1

    aAM = np.array([math.log(AM[i][j]) for i in range(len(AM)) for j in range(len(AM))])

    mAM = np.mean(aAM)
    sAM = np.std(aAM)

    lAM = [[0 for i in range(len(TOP))] for j in range(len(TOP))]

    for i in range(len(lAM)):
        for j in range(i):
            if math.log(AM[i][j]) > mAM + 2.5*sAM:
                lAM[i][j] = 1
                lAM[j][i] = 1

    return AM, lAM

def generateDATA(name, TOP, dDIFF):

    DATA = {}

    DATA['nodes'] = []
    DATA['links'] = []        

    for item in TOP.keys():
        dn = {}
        dn['id'] = name + '_' + item
        dn['name'] = item
        dn['playcount'] = -dDIFF[item]*100
        dn['artist'] = name
        dn['match'] = random.random()

        DATA['nodes'].append(dn)

    for i in range(len(TOP)):
        for j in range(i):

            if lAM[i][j]>0:
                dl = {}
                dl['source'] = name + '_' + TOP.keys()[i]
                dl['target'] = name + '_' + TOP.keys()[j]
                DATA['links'].append(dl)



    with open('DATA/TOPICS_' + name+ '.json','wb') as outfile:
        json.dump(DATA, outfile)


"""
