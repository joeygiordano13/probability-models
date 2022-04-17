# models.py
# import sys
import pandas as pd
import numpy as np
import random
import typing
from matplotlib import pyplot as plt

WIN = 1
LOSE = 0
DRAW = -1
NUM_RUNS = 5
MAX_STEPS = 1000

def sim(p: int, start: int, goal: int, iter: int) -> typing.Tuple[int, bool, pd.DataFrame]:
    """
    Run main simulation. 
    Args:
        p: (int) probability of success for each step
        start: (int) how much money you start with
        goal: (int) the upper bound of cash where you stop
        iter: (int) iteration of sim
    Returns: 
        time_to_end: (int) number of steps to reach boundary condition
        success: (bool) reached upper bound, or lost all money
        df: (pd.DataFrame) dataframe to append cash walk timesteps
    Note: 
        change return types in Python3.9 to -> tuple[int, bool]
    """
    print(f"Running gambling simulation...")

    t = 0 # init step
    steps = np.array([])
    cash = start
    # simulation loop
    while (t < MAX_STEPS):
        rand = float(random.random())
        state = WIN if rand < p else LOSE # determine round result
        cash += 1 if state is WIN else -1 # update cash
        steps = np.append(steps, cash)
        t += 1
        # end simulation condition
        if cash >= goal or cash <= 0:
            df = pd.DataFrame(steps, columns=[f"Walk {iter}"])
            return (t, WIN, df) if cash > 0 else (t, LOSE, df)
    # exceeded max steps
    df = pd.DataFrame(steps, columns=[f"Walk {iter}"])
    return (t, DRAW, df)

def display_plots(df, goal):
    """
    Plots a series of columns in one graph
    Args:
        df: (pd.DataFrame) dataframe with all the cash walks you want to plot
    """
    plt.plot(df) #plotting all the cash walks
    plt.title('Cash Walks') # plot title
    plt.xlabel('Step')  # x axis label
    plt.ylabel('Cash Amount')   # y axis label
    plt.xticks(range(0, MAX_STEPS, int(MAX_STEPS/10)))
    plt.yticks(range(0, goal, int(goal/10)))
    plt.xlim(0, MAX_STEPS) #sets the x axis bounds displayed
    plt.ylim(0, goal) #sets the y axis bounds displayed
    plt.legend(['Walk ' + str(num) for num in range(df.shape[1])])    #the legend of the plot
    plt.show()  # makes plot visible
    plt.savefig("walks.eps", format='eps')  # saves plot to file
    

def main(numiter):
    print(f"In main, calling gambling sim {numiter} times")
    p = float(input("Probability of success per round: "))
    start = int(input("Starting money: "))
    goal = int(input("Goal money: "))
   
    end_times = []
    end_states = []

    df = pd.DataFrame()

    # time: int
    # state: int
    # Running simulation N times
    for i in range(numiter): 
        time, state, df_out = sim(p, start, goal, i)
        end_times.append(time)
        end_states.append(state)
        df = pd.concat([df, df_out])
    # Print output
    print('\n')
    for i in range(numiter):
        print(f"Iter {i}: time - {end_times[i]} state - {'WIN' if end_states[i] is WIN else 'LOSE' if end_states[i] is LOSE else 'DRAW'}")
        
    # Displays statistics from the walks
    print('\n')
    print(df.describe())
    # Display output in matplot
    print('\n')
    display_plots(df, goal)
    
    print(f'Average Walk End: {np.mean(end_times)}')
    
    wins = np.sum(pd.Series(end_states) > 0)
    print(f'Win Rate: {wins}/{numiter} = {wins/numiter}')
    print('\n')
    
if __name__ == "__main__":
    main(NUM_RUNS) # iterations
