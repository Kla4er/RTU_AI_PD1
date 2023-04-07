
# Graph
G = [] # Edges
Vecr = [] # Conditions (N; BestNextVerc)
Size = 0 # Size of verc in graph

# Recursive graph creating with specific depth
def createGraph(N, K, depth):
    if depth == 0:
        return -1
    if N < 0:
        return -1

    global Size, Vecr, G
    cursize = Size
    Vecr.append([])
    Vecr[cursize].append((N, -1)) # Add new vertex to graph - {N = count of the stick; -1 - The best way for AI}
    G.append([])
    Size += 1
    for i in range(1, K + 1): # Recursive creating next lvl of vertexes
        child = createGraph(N - i, K, depth-1) # N-1; N-2 ... N-K
        if child != -1:
            G[cursize].append(child)
    return cursize

# Heuristic valuation function
# loose condition for current player is only N % (K+1) == 0 condition.
def Valuate(N, K, isMaxLvl):
    if isMaxLvl:
        if N % (K+1) == 0:
            return -1
        return 1
    else:
        if N % (K+1) == 0:
            return 1
        return -1

# Best step finding - Minimaksa algorithm
def FindBest(verc, isMaxLvl, K):
    global Vecr, G
    if not G[verc]:
        return Valuate(Vecr[verc][0][0], K, isMaxLvl) # Valuate by heuristic function
    answ = None # best condition for current player
    for u in G[verc]:
        child = FindBest(u, not isMaxLvl, K) # Find all best conditions in children vertexes
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
    createGraph(N, K, 5) # Create graph from the currect condition
    FindBest(0, True, K) # Find the best way
    return Vecr[0][0][0] - Vecr[Vecr[0][0][1]][0][0]  # curent position N - the best step condition N