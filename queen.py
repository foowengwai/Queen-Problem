import random
import statistics
import pandas as pd
import matplotlib.pyplot as plt
# board = [1, 3, 5, len(board)-1, 2, 4, 6, len(board)] # this is row and value is its column, cuz the other way around is annoying
# board = [len(board), 6, 4, 2, len(board)-1, 5, 3, 1] # this is row and value is its column, cuz the other way around is annoying
# board = [1, len(board)-1, 5, len(board), 2, 4, 6, 3] # this is row and value is its column, cuz the other way around is annoying

def objFunc(board):
    cost = 0
    # check for same col
    colFail = 0
    for row in range(1,len(board)+1):
        count = board.count(row)
        if count != 1:
            colFail += 1 
    # print("no of dupe: ", colFail)
    
 
 
    # check for diagonal
    diaFail = 0
    for row in range(len(board)):
        for col in range(len(board[row::])):
            rowDif = abs(board[row+col] - board[row])
            iDif = (row+col) - row
            if rowDif == iDif and (rowDif or iDif)!=0:
                diaFail += 1
    # print("no of dia met: ", diaFail)
    cost = colFail + diaFail
    return cost


#################
##  Utilities  ##
#################

def getStats(data):
    costs = data[0]
    iterations = data[1]
    
    iMin = min(iterations)
    iMode = statistics.mode(iterations)
    iMedian = statistics.median(iterations)
    iMean = statistics.mean(iterations)
    iMax = max(iterations)
    
    cMin = min(costs)
    cMode = statistics.mode(costs)
    cMedian = statistics.median(costs)
    cMean = statistics.mean(costs)
    cMax = max(costs)
    
    solvedIterations = []
    for i in range(len(costs)):
        if costs[i] == 0:
            solvedIterations.append(iterations[i])
    nfe = statistics.median(solvedIterations)
    
    founds = costs.count(0)
    foundsPersent = costs.count(0)/len(costs)*100
    
    return iMin, iMode, iMedian, iMean, iMax, cMin, cMode, cMedian, cMean, cMax, founds, foundsPersent, nfe

def compare(runs, iterations, bit, **algorithms):
    # print(f"\t\t\t\tIMin\tIMode\tIMed\tIMean\tIMax\tCMin\tCMode\tCMed\tCMean\tCMax\tFounds\tFounds (%)\tNFE")
    print(f"\t\t\t\tFounds\t\tFounds (%)\tNFE")
    raw_df_data = []
    for name, algorithm in algorithms.items():
        # 0 is cost, 1 is iter
        searchData = [[], []]
        for _ in range(runs):
            _, cost, iteration = algorithm(iterations, bit)
            searchData[0].append(cost)
            searchData[1].append(iteration)
        stat = getStats(searchData)
        print(name, "\t\t".join(f"{round(x, 2):g}" for x in stat[10::]), sep='\t')
        
        # Compile data to pandas for plot
        filteredStat = [stat[0:5], stat[5:10]]
        for i in range(2):
            row_data = {
                "Loop_Name": name.strip("\t") + f" ({"Cost" if i == 0 else "Iteration"})",
                "Min": filteredStat[i][0],
                "Mode": filteredStat[i][1],
                "Median": filteredStat[i][2],
                "Mean": filteredStat[i][3],
                "Max": filteredStat[i][4]
            }
            raw_df_data.append(row_data)
    df = pd.DataFrame(raw_df_data)
    plotGraph(df)


def plotGraph(df):
    # Split DataFrame into Cost and Iteration subsets based on Loop_Name
  cost_df = df[df['Loop_Name'].str.contains(r'\(Cost\)', regex=True)].copy()
  iter_df = df[
      df['Loop_Name'].str.contains(r'\(Iteration\)', regex=True)
  ].copy()

  # Clean labels by removing '(Cost)' and '(Iteration)' for cleaner axes
  cost_df['Clean_Name'] = cost_df['Loop_Name'].str.replace(
      ' (Cost)', '', regex=False
  )
  iter_df['Clean_Name'] = iter_df['Loop_Name'].str.replace(
      ' (Iteration)', '', regex=False
  )

  fig, axes = plt.subplots(1, 2, figsize=(15, 6))

  datasets = [
      (axes[0], cost_df, 'Algorithm Cost Comparison', 'Cost'),
      (axes[1], iter_df, 'Algorithm Iteration Comparison', 'Iterations'),
  ]

  for ax, sub_df, title, ylabel in datasets:
    bxp_stats = []
    for _, row in sub_df.iterrows():
      # Approximate Q1 and Q3 as midpoints between Min/Median and Median/Max
      q1 = (row['Min'] + row['Median']) / 2
      q3 = (row['Median'] + row['Max']) / 2

      bxp_stats.append({
          'label': row['Clean_Name'],
          'whislo': row['Min'],
          'q1': q1,
          'med': row['Median'],
          'q3': q3,
          'whishi': row['Max'],
          'mean': row['Mean'],
      })

    # Draw the pre-calculated boxes
    ax.bxp(
        bxp_stats,
        showmeans=True,
        showfliers=False,
        patch_artist=True,
        boxprops={'facecolor': '#e0f3f8', 'edgecolor': '#333333'},
        medianprops={'color': '#d95f02', 'linewidth': 2, 'label': 'Median'},
        meanprops={
            'marker': 'o',
            'markerfacecolor': '#1b9e77',
            'markeredgecolor': 'black',
            'markersize': 7,
            'label': 'Mean',
        },
    )

    # Overlay the Mode values
    x_positions = range(1, len(sub_df) + 1)
    ax.scatter(
        x_positions,
        sub_df['Mode'],
        color='#7570b3',
        marker='D',
        s=50,
        zorder=4,
        label='Mode',
    )

    # Formatting and labels
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=30)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Deduplicate legend items
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys(), loc='best')

  plt.tight_layout()
  plt.show()
        
# fancy board
def printBoard(board):
    print("      1   2   3   4   5   6   7   8")
    print("    ┌───⁠┬───┬───┬───┬───┬───┬───┬───┐")
    for row in range(1, len(board)+1):
        # print("│ │ │ │ │ │ │ │ │", end='')
        print(row, " ", end=' ') # col numbering
        for col in range(1, len(board)+1):
            print("│", end=' ')
            if col == board[row-1]:
                print("♛", end=" ")
            else:
                print(" ", end=" ")
        print("│")
        if row == len(board):
            print("    └───┴───┴───┴───┴───┴───┴───┴───┘⁠")
        else:
            print("    ├───┼───┼───┼───┼───┼───┼───┼───┤")   



##################
##  Algorithms  ##
##################

def randomSearch(maxIterations=1000, bit=8):
    bestBoard = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(bestBoard)
    iteration = 0
    if bestCost == 0: # if it randomly finds one
            return bestBoard, bestCost, iteration
    
    for i in range(maxIterations):
        newBoard = random.sample(range(1,len(bestBoard)+1), len(bestBoard))
        newCost = objFunc(newBoard)
        # print("new best board: ", bestBoard, " with cost: ", bestCost)
        # print("new board: ", newBoard, " with cost: ", newCost)
        if newCost < bestCost:
            bestCost = newCost
            bestBoard = newBoard.copy()
            if bestCost == 0:
                break
        iteration += 1
    return bestBoard, bestCost, iteration

def hillClimbSearch(maxIterations=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0
    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration
    
    for i in range(maxIterations):
        changingPos = random.randint(0, len(board)-1)
        newBoard = board.copy()
        newBoard[changingPos] = random.randint(1, len(board))
        newCost = objFunc(newBoard)
        if newCost <= bestCost: # if cost is lesser
            board = newBoard.copy()
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1
    return board, bestCost, iteration

def swapHillClimbSearch(maxIteration=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0

    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration

    for _ in range(maxIteration):
        swapA = random.randint(0, len(board)-1)
        swapB = random.randint(0, len(board)-1)
        newBoad = board.copy()
        newBoad[swapA] = board[swapB]
        newBoad[swapB] = board[swapA]
        newCost = objFunc(newBoad)
        if newCost <= bestCost:
            board = newBoad.copy()
            # print('#', i, newBoad, swapA+1, swapB+1)
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1

    return board, bestCost, iteration

def neighborSwapHillClimbSearch(maxIteration=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0

    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration

    for _ in range(maxIteration):
        pivot = random.randint(1, len(board)-2)
        newBoad = board.copy()
        newBoad[pivot+1] = board[pivot-1]
        newBoad[pivot-1] = board[pivot+1]
        newCost = objFunc(newBoad)
        if newCost <= bestCost:
            board = newBoad.copy()
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1

    return board, bestCost, iteration

def simulatedAnnealing(maxIteration=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0

    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration

    for _ in range(maxIteration):
        swapA = random.randint(0, len(board)-1)
        swapB = random.randint(0, len(board)-1)
        passThrough = random.random()
        newBoad = board.copy()
        newBoad[swapA] = board[swapB]
        newBoad[swapB] = board[swapA]
        newCost = objFunc(newBoad)
        if newCost <= bestCost or passThrough > threshole:
            board = newBoad.copy()
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1

    return board, bestCost, iteration

def neighborSimulatedAnnealing(maxIteration=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0

    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration

    for _ in range(maxIteration):
        passThrough = random.random()
        pivot = random.randint(1, len(board)-2)
        newBoad = board.copy()
        newBoad[pivot+1] = board[pivot-1]
        newBoad[pivot-1] = board[pivot+1]
        newCost = objFunc(newBoad)
        if newCost <= bestCost or passThrough > threshole:
            board = newBoad.copy()
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1

    return board, bestCost, iteration

def swapRandomSearch(maxIteration=1000, bit=8):
    board = random.sample(range(1,bit+1), bit)
    bestCost = objFunc(board)
    iteration = 0

    if bestCost == 0: # if it randomly finds one
        return board, bestCost, iteration

    for _ in range(maxIteration):
        swapA = random.randint(0, len(board)-1)
        swapB = random.randint(0, len(board)-1)
        newBoad = board.copy()
        newBoad[swapA] = board[swapB]
        newBoad[swapB] = board[swapA]
        newCost = objFunc(newBoad)
        board = newBoad.copy()
        if newCost < bestCost:
            bestCost = newCost
            if bestCost == 0:
                break
        iteration += 1

    return board, bestCost, iteration



threshole = .9
algorithms = {
    "Random (Fully)\t\t": randomSearch,
    "Random (Swap)\t\t": swapRandomSearch,
    "Hill Climb (Random)\t": hillClimbSearch,
    "Hill Climb (Swap)\t": swapHillClimbSearch,
    "Hill Climb (Swap neighbor)": neighborSwapHillClimbSearch,
    "Simulated Annealing\t": simulatedAnnealing,
    "Simulated Annealing (neighbor)": neighborSimulatedAnnealing,
}
compare(runs=50, iterations=1000, bit=8, **algorithms)






# randomSearchBoard, randomSearchCost, randomSearchIteration = randomSearch()
# print("Random Search cost:", randomSearchCost, ", in iteration:", randomSearchIteration)
# printBoard(randomSearchBoard)

# print()

# hillClimbSearchBoard, hillClimbSearchCost, hillClimbSearchIteration = hillClimbSearch()
# print("Hill Climb cost:", hillClimbSearchCost, ", in iteration:", hillClimbSearchIteration)
# printBoard(hillClimbSearchBoard)

# print()

# swapHillClimbSearchBoard, swapHillClimbSearchCost, swapHillClimbSearchIteration = swapHillClimbSearch()
# print("Swap Hill Climb cost:", swapHillClimbSearchCost, ", in iteration:", swapHillClimbSearchIteration)
# printBoard(swapHillClimbSearchBoard)