# Graph
G = []  # Edges
Vecr = [] # Conditions (N; BestNextVerc)
Size = 0 # Size of verc in graph


# Recursive graph creating from current position to the bottom
def createGraph(N, K):
    if N < 0:
        return -1

    global Size, Vecr, G
    cursize = Size
    # Check does Vecr[] already have current condition
    for i in range(0,len(Vecr)):
        if Vecr[i][0][0] == N: # if has - is not necessary create new node
            return i
    Vecr.append([])
    Vecr[cursize].append((N, -1)) # Add new vertex to graph - {N = count of the stick; -1 - The best way for AI}
    G.append([])
    Size += 1
    for i in range(1, K + 1): # Recursive creating next lvl of vertexes
        child = createGraph(N - i, K)  # N-1; N-2 ... N-K
        if child != -1:
            G[cursize].append(child)
    return cursize

# Best step finding - Minimaksa algorithm
def FindBest(verc, isMaxLvl):
    global Vecr, G, BestStep

    if not G[verc]: # If current vertex is a list - it is the end of the game
        if isMaxLvl:
            return -1
        else:
            return 1
    answ = None
    for u in G[verc]: # Find all best conditions in children vertexes
        child = FindBest(u, not isMaxLvl) # Find all best conditions in children vertexes
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
    createGraph(N, K)  # Create graph from the currect condition
    FindBest(0, True) # Find the best way
    return Vecr[0][0][0] - Vecr[Vecr[0][0][1]][0][0] # curent position N - the best step condition N