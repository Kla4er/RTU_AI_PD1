
# Graph
G = [] # Edges
Vecr = [] # Conditions (N; BestNextVerc)
Size = 0 # Size of verc in graph


def createGraph(N, K, depth):
    if depth == 0:
        return -1
    if N < 0:
        return -1

    global Size, Vecr, G
    cursize = Size
    Vecr.append([])
    Vecr[cursize].append((N, -1))
    G.append([])
    Size += 1
    for i in range(1, K + 1):
        child = createGraph(N - i, K, depth-1)
        if child != -1:
            G[cursize].append(child)
    return cursize

def Valuate(N, K, isMaxLvl):
    if isMaxLvl:
        if N % (K+1) == 0:
            return -1
        return 1
    else:
        if N % (K+1) == 0:
            return 1
        return -1

def FindBest(verc, isMaxLvl, K):
    global Vecr, G
    if not G[verc]:
        return Valuate(Vecr[verc][0][0], K, isMaxLvl) # Valuate by hirestic function
    answ = None
    for u in G[verc]:
        child = FindBest(u, not isMaxLvl, K)
        if answ == None:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u)
            continue
        if isMaxLvl and answ < child:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u) # (N, -1)
        if not isMaxLvl and answ > child:
            answ = child
            Vecr[verc][0] = (Vecr[verc][0][0], u) # (N, -1)
    return answ

def getnewK(N,K):
    global G, Vecr, Size
    G = []
    Vecr = []
    Size = 0
    createGraph(N, K, 5)
    FindBest(0, True, K)
    return Vecr[0][0][0] - Vecr[Vecr[0][0][1]][0][0]  # (Vecr[verc][0][0], u)