# Graph
G = []
Vecr = []
Size = 0

def createGraph(N, K):
    if N < 0:
        return -1

    global Size, Vecr, G
    cursize = Size
    Vecr.append([])
    Vecr[cursize].append((N, -1))
    G.append([])
    Size += 1
    for i in range(1, K + 1):
        child = createGraph(N - i, K)
        if child != -1:
            G[cursize].append(child)
    return cursize


def FindBest(verc, isMaxLvl):
    global Vecr, G, BestStep

    if not G[verc]:
        if isMaxLvl:
            return -1
        else:
            return 1
    answ = None
    for u in G[verc]:
        child = FindBest(u, not isMaxLvl)
        if answ == None:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u)
            continue
        if isMaxLvl and answ < child:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u)
        if not isMaxLvl and answ > child:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u)
    return answ


def getnewK(N,K):
    global G, Vecr, Size
    G = []
    Vecr = []
    Size = 0
    createGraph(N, K)
    FindBest(0, True)
    return Vecr[0][0][0] - Vecr[Vecr[0][0][1]][0][0]