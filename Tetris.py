import sys
import random
import pickle

global OFFSETS,PIECESDIM,PIECES
#setup pieces
OFFSETS = {"I0":(0,0,0,0),"I1":(0,),"O0":(0,0),"T0":(0,0,0),"T1":(0,-1),"T2":(-1,0,-1),"T3":(-1,0),"S0":(0,0,-1),"S1":(-1,0),"Z0":(-1,0,0),"Z1":(0,-1),"J0":(0,0,0),"J1":(0,-2),"J2":(-1,-1,0),"J3":(0,0),"L0":(0,0,0),"L1":(0,0),"L2":(0,-1,-1),"L3":(-2,0)}
PIECESDIM = {'I0':(4,1), 'I1':(1,4), 'O0':(2,2), 'T0':(3,2), 'T1':(2,3), 'T2':(3,2), 'T3':(2,3), 'S0':(3,2), 'S1':(2,3), 'Z0':(3,2), 'Z1':(2,3), 'J0':(3,2), 'J1':(2,3), 'J2':(3,2), 'J3':(2,3), 'L0':(3,2), 'L1':(2,3), 'L2':(3,2), 'L3':(2,3)} #:(width,height)
PIECES = {'I0':[(0,0),(1,0),(2,0),(3,0)], 'I1':[(0,0),(0,1),(0,2),(0,3)], 'O0':[(0,0),(0,1),(1,0),(1,1)], 'T0':[(0,0),(1,0),(1,1),(2,0)], 'T1':[(0,0),(0,1),(0,2),(1,1)], 'T2':[(0,1),(1,0),(1,1),(2,1)], 'T3':[(0,1),(1,0),(1,1),(1,2)], 'S0':[(0,0),(1,0),(1,1),(2,1)], 'S1':[(0,1),(0,2),(1,0),(1,1)], 'Z0':[(0,1),(1,0),(1,1),(2,0)], 'Z1':[(0,0),(0,1),(1,1),(1,2)], 'J0':[(0,0),(0,1),(1,0),(2,0)], 'J1':[(0,0),(0,1),(0,2),(1,2)], 'J2':[(0,1),(1,1),(2,1),(2,0)], 'J3':[(0,0),(1,0),(1,1),(1,2)], 'L0':[(0,0),(1,0),(2,0),(2,1)], 'L1':[(0,0),(0,1),(0,2),(1,0)], 'L2':[(0,0),(0,1),(1,1),(2,1)], 'L3':[(0,2),(1,0),(1,1),(1,2)]} #bot left is origin
def printBoard(board):
    out = ""
    for i in range(0,200,10):
        out += str(19 - i//10) + "\t" + board[i:i+10]+ "\n"
    print(out)

def boardHeights(board): #max of each column, and offset hardcoded
    colHeights = {i:0 for i in range(0,10)}
    for i in range(0,10):
        for j in range(i,i+200,10):
            if board[j] == "#":
                colHeights[i]+= 20 - j//10
                break
    return colHeights

def insertPiece(board,piece,inCol): #both row and col start at 0
    colHeights = boardHeights(board)
    tempHeights = []
    for i in range(inCol,inCol+PIECESDIM[piece][0]):
        tempHeights.append(colHeights[i]+OFFSETS[piece][i-inCol])
    inRow = max(tempHeights)
    if(inRow+PIECESDIM[piece][1])>20:
        return ("GAME OVER",0)
    #now insert the piece
    coords = PIECES[piece]
    for i in coords:
        x,y = i
        x1 = inCol + x
        y1 = 19-(inRow + y)
        pos = x1 + 10*y1
        board = board[0:pos]+ "#" + board[pos+1:]
    board,count = elimRow(board)
    return (board,count)

def elimRow(board):
    count = 0
    temp = []
    for i in range(0,200,10):
        temp.append(board[i:i+10])
    completeRow = "##########"
    while completeRow in temp:
        temp.remove(completeRow)
        count+=1
    out = ""
    for i in range(count):
        out+="          "
    out+="".join(temp)
    return (out,count)

def allPossibles(board):
    out = ""
    for p in PIECES.keys():
        for col in range(0,10-PIECESDIM[p][0]+1):
            out += insertPiece(board,p,col) + "\n"
    return out

# modeling
# test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"

# with open("tetrisout.txt",'w') as f:
#     f.write(allPossibles(sys.argv[1]))

global PIECEORG
PIECEORG = {"I":["I0","I1"],"O":["O0"],"T":["T0","T1","T2","T3"],"S":["S0","S1"],"Z":["Z0","Z1"],"J":["J0","J1","J2","J3"],"L":["L0","L1","L2","L3"]}

def play_game(strategy):
    board = " ".join(["" for i in range (0,201)])
    points = 0
    while board != "GAME OVER":
        poss = []
        piece = list(PIECEORG.keys())[random.randint(0,len(PIECEORG.keys())-1)]
        #print(piece)
        for orient in PIECEORG[piece]:
            for col in range(0,10-PIECESDIM[orient][0]+1):
                poss_board, poss_board_elims = insertPiece(board,orient,col)
                poss_score = heuristic(poss_board, strategy, poss_board_elims)
                poss.append((poss_score,poss_board,poss_board_elims))
        poss.sort(reverse=True)
        temp,board,elims = poss[0]
        #print(poss[0])
        #print(board)
        if elims > 0:
            if elims == 1:
                points += 40 #reminder: 1 row cleared --> 40 points, 2 --> 100, 3 --> 300, 4 --> 1200
            if elims == 2:
                points += 100
            if elims == 3:
                points += 300
            if elims == 4:
                points += 1200
        #print(points)
    return points

def print_play_game(strategy):
    board = " ".join(["" for i in range (0,201)])
    points = 0
    while board != "GAME OVER":
        poss = []
        piece = list(PIECEORG.keys())[random.randint(0,len(PIECEORG.keys())-1)]
        #print(piece)
        for orient in PIECEORG[piece]:
            for col in range(0,10-PIECESDIM[orient][0]+1):
                poss_board, poss_board_elims = insertPiece(board,orient,col)
                poss_score = heuristic(poss_board, strategy, poss_board_elims)
                poss.append((poss_score,poss_board,poss_board_elims))
        poss.sort(reverse=True)
        temp,board,elims = poss[0]
        #print(poss[0])
        #print(board)
        if elims > 0:
            if elims == 1:
                points += 40 #reminder: 1 row cleared --> 40 points, 2 --> 100, 3 --> 300, 4 --> 1200
            if elims == 2:
                points += 100
            if elims == 3:
                points += 300
            if elims == 4:
                points += 1200
        printBoard(board)
        print("Current score: " + str(points))
        print()
    return points

def heuristic(board, strategy, elims):
    if board == "GAME OVER":
        return -9999

    a, b, c, d = strategy 
    value = 0

    heights = list(boardHeights(board).values())
    value += a * max(heights) #(perhaps highest column height?)

    wells = []
    for i in range(0,len(heights)):
        if i == 0 and heights[1]>heights[0]:
            wells.append(heights[1]-heights[0])
        elif i == len(heights) - 1 and heights[i-1]>heights[i]:
            wells.append(heights[i-1] - heights[i])
        elif heights[i-1]>heights[i] and heights[i+1]>heights[i]:
            wells.append(max(heights[i-1],heights[i+1])-heights[i])
    if len(wells)>0:
        value += b * max(wells) #(perhaps deepest well depth?)

    holes = 0
    for i in range(10,len(board)):
        if board[i] == " " and board[i-10] == "#":
            holes += 1
    value += c * holes #(perhaps number of holes in board, ie empty spaces with a filled space above?)

    value += d * elims #(perhaps the number of lines that were just cleared, in the move that made this board?)
    return value

# for i in range(0,500):
#     print(play_game((1,1,1,1)))

global POPULATION_SIZE, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE

POPULATION_SIZE = 300
NUM_CLONES = 5
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
#CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

def population(n):
    out = []
    for i in range(0,n):
        temp = (random.randint(-100,100),random.randint(-100,100),random.randint(-100,100),random.randint(-100,100))
        fitemp = fitness(temp)
        print("Evaluating strategy number " + str(i) + " --> " + str(fitemp))
        out.append((fitemp,temp)) #stored as (fitness,(strat))
    out.sort(reverse=True)
    print("Average: " + str(sum(x[0] for x in out)/len(out)))
    print("Best strategy so far: " + str(out[0][1]) + " with score: " + str(out[0][0]))
    print("Geneneration: 0")
    print()
    return out

def fitness(strategy):
    game_scores = []
    for count in range(0,5):
        game_scores.append(play_game(strategy))
    return sum(game_scores) / len(game_scores)

def selection(strats,gen):
    num = 0
    nGen = []
    rank = strats
    rank.sort(reverse=True)
    for i in range (0,NUM_CLONES):
        nGen.append(rank[i])
        print("Evaluating strategy number " + str(num) + " --> " + str(rank[i][0]))
        num+=1
    while(len(nGen)<POPULATION_SIZE):   
        rGen = rank
        random.shuffle(rGen)
        t1 = rGen[0:TOURNAMENT_SIZE]
        t2 = rGen[TOURNAMENT_SIZE:TOURNAMENT_SIZE*2]
        t1.sort(reverse=True)
        t2.sort(reverse=True)
        i1 = random.random()
        while(i1 > TOURNAMENT_WIN_PROBABILITY and len(t1)>2):
            t1.pop(0)
            i1 = random.random()
        i2 = random.random()
        while(i2 > TOURNAMENT_WIN_PROBABILITY and len(t2)>2):
            t2.pop(0)
            i2 = random.random()
        temp = mutation(breeding(t1[0][1],t2[0][1]))
        if temp not in nGen:
            fitemp = fitness(temp)
            nGen.append((fitemp,temp))
            print("Evaluating strategy number " + str(num) + " --> " + str(fitemp))
            num+=1
    nGen.sort(reverse=True)
    print("Average: " + str(sum(x[0] for x in nGen)/len(nGen)))
    print("Best strategy so far: " + str(nGen[0][1]) + " with score: " + str(nGen[0][0]))
    print("Geneneration: " + str(gen))
    print()
    return(nGen,gen+1)
    selection(nGen,gen+1)


def breeding(strat1,strat2):
    s1 = list(strat1)
    s2 = list(strat2)
    child = []
    for i in range(0,len(s1)):
        child.append(-9999)
    for i in random.sample(range(0,len(s1)),random.randint(1,len(s1)-1)):
        child[i]=s1[i]
    while -9999 in child:
        ind = child.index(-9999)
        child[ind]=s2[ind]
    return tuple(child)

def mutation(strat):
    i = random.random()
    temp = list(strat)
    if(i<MUTATION_RATE):
        ind = random.randint(0,len(strat)-1)
        new = random.randint(-100,100)
        temp[ind]=new
    return tuple(temp)

#user input 
start = input ("(N)ew process, or (L)oad saved process?")
temp = []
gen = 1
if start == "N":
    temp = population(POPULATION_SIZE)
if start == "L":
    filename = input("What filename?")
    infile = open(filename,'rb')
    gen,temp = pickle.load(infile)
    print("Geneneration: " + str(gen))
    print("Best strategy so far: " + str(temp[0][1]) + " with score: " + str(temp[0][0]))
next = input("(P)lay a game with current best strategy, (S)ave current progress, or (C)ontinue?")
while(next != "S"):
    if next == "C":
        temp,gen = selection(temp,gen)
    if next == "P":
        print_play_game(temp[0][1])
    next = input("(P)lay a game with current best strategy, (S)ave current progress, or (C)ontinue?")
    if next == "S":
        filename = input("What filename?")
        outfile = open(filename,'wb')
        pickle.dump((gen,temp),outfile)
        outfile.close()
        print()
        print("Process finished with exit code 0")
        print()
        sys.exit(0)

