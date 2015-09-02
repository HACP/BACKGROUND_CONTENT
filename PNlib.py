import pylab as P
import numpy as np
import random, math

def generateNetwork(aINDEX, dDIFF, AM, name):
    R = 100
    X = []
    Y = []
    Z = []

    for i in range(len(aINDEX)):
        #r = 100*R + sum(AM[i])*R
        r = 1000*R + 10000*abs(dDIFF[aINDEX[i]])*R
        t = 2*math.pi*random.random()
        X.append(r*math.cos(t))
        Y.append(r*math.sin(t))
        Z.append(sum(AM[i]))

    fig = P.figure()

    P.axis('off')
    P.scatter(X, Y, Z, edgecolor = '', c = 'lightblue', alpha = 0.5)

    for i in range(len(aINDEX)):
        for j in range(i):
            if sum(AM[i]) > 200 and sum(AM[j]) > 200:
                P.plot([X[i], X[j]], [Y[i], Y[j]],'k',lw = 0.01)

    for i in range(len(aINDEX)):
        if sum(AM[i])>200:
    
            P.text(X[i], Y[i], aINDEX[i], fontsize = 8)
        

    #P.show()
    fig.savefig('figures/' + name + '.png')
    return

def plotTOPICS(name, sdDIFF, dKT):

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

    fig = P.figure()
    P.scatter(X, Y)
    fig.savefig('figures/DISTR_' + name + '.png') 

    return X, Y
