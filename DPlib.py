import json, math, csv, random
import numpy as np


def getBG():
    with open('DATA/topics_agg.json') as json_file:
        json_data = json.load(json_file)
        L1 = json_data['aggregations']['my_agg']['buckets']

        S = []
        K = []
        for item in L1:
            #print item['key'], item['doc_count']
            S.append(int(item['doc_count']))
            K.append(item['key'])
        
    TOT = sum(S)
    lS = [math.log(1.*item/TOT) for item in S]

    dlS = {}
    for i in range(len(lS)):
        dlS[K[i]] = -lS[i]
    return dlS

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

    aKT = {x:KT.count(x) for x in list(set(KT))}

    sdKT =  sorted(dKT.items(), key=lambda x: x[1])

    return dKT, lKT, sdKT, aKT

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

def generateDATA(name, TOP, dDIFF, dKT, aKT, lAM, AM):
    
    lDATA = []
    eDATA = []

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
        dn['freq'] = dKT[item]

        DATA['nodes'].append(dn)

        lDATA.append([item, -dDIFF[item]*100, aKT[item]])

    for i in range(len(TOP)):
        for j in range(i):

            if lAM[i][j]>0:
                dl = {}
                dl['source'] = name + '_' + TOP.keys()[i]
                dl['target'] = name + '_' + TOP.keys()[j]
            
                DATA['links'].append(dl)
                eDATA.append([TOP.keys()[i], TOP.keys()[j], math.sqrt(dDIFF[TOP.keys()[i]]*dDIFF[TOP.keys()[j]])*100, AM[i][j]])


    with open('DATA/TOPICS_' + name+ '.json','wb') as outfile:
        json.dump(DATA, outfile)


    slDATA = sorted(lDATA, key=lambda x: x[1], reverse=True)
    seDATA = sorted(eDATA, key=lambda x: x[2], reverse=True)
    
    """
    for item in seDATA:
        print item[0], ',', item[1], ',', item[2], ',', item[3]
    
    """
    for item in lDATA:
        print item
    
