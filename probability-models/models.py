# models.py
# import sys
from tracemalloc import start
import pandas as pd
import numpy as np
import random
import typing
from matplotlib import pyplot as plt

PROB_WIN = 0.64
START_MONEY = 50
GOAL_MONEY = 100

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
        t += 1 # increment timesteps
        # end simulation condition
        if cash >= goal or cash <= 0:
            df = pd.DataFrame(steps, columns=[f"run-{iter}"])
            return (t, WIN, df) if cash > 0 else (t, LOSE, df) 
    # exceeded max steps
    df = pd.DataFrame(steps, columns=[f"run-{iter}"])
    return (t, DRAW, df)

# Todo: add types
def display_plots(df, times, exp_time):
    """
    Plots a series of columns in one graph
    Args:
        df: (pd.DataFrame) dataframe with all the cash walks you want to plot
    """

    plt.plot(df)
    plt.title('Cash Walks') # plot title
    plt.xlabel('Step')  # x axis label
    plt.ylabel('Cash Amount')   # y axis label
    plt.xlim(0, MAX_STEPS)
    plt.ylim(0, 100)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.legend(['Walk ' + str(num) for num in range(df.shape[1])] + [' time ' + str(time) for time in times]) # legend 
    # Print expected time
    plt.text(0, 110, f"Expected time: {abs(int(exp_time))}", fontsize=12)
    # Print actual times
    plt.text(0, 107, [str(entry) for entry in times], fontsize=12)
    plt.savefig("walks.eps", format='eps')  # saves plot to file
    plt.show()  # makes plot visible  

# T_j is the first time a particle arrives at 0 or N when it
# starts at j
def compute_expected_time_to_boundary(p: float, j: int, N: int) -> float:
    """
        Computes the expected time to reach a boundary state (lose
        all money or reach goal), given a starting point and probability
        of winning each round in the gambling game.
        Args:
            p: (float) probability to win a game
            j: starting point
            N: goal
    """
    q = 1 - p # prob lose
    # general solution to
    # homogeneous equation 4.7
    if p == q:
        return (j * (N - j))
    else:
        return (1 / (q - p)) * (j - (N * ((1 - pow((q / p), j) / (1 - pow((q / p), N))))))


def main(numiter):
    print(f"In main, calling gambling sim {numiter} times")
    #p = float(input("Probability of success per round: "))
    #start = int(input("Starting money: "))
    #goal = int(input("Goal money: "))
    p = PROB_WIN
    start = START_MONEY
    goal = GOAL_MONEY
    end_times = []
    end_states = []
    df = pd.DataFrame()

    # Running simulation N times
    for i in range(numiter): 
        time, state, df_out = sim(p, start, goal, i)
        end_times.append(time)
        end_states.append(state)
        df = pd.concat([df, df_out])
    # Print output
    for i in range(numiter):
        print(f"Iter {i}: time - {end_times[i]} state - {'WIN' if end_states[i] is WIN else 'LOSS'}")
    # Compute expected time to boundary
    boundary_pred =  compute_expected_time_to_boundary(p, start, goal)
    # Display output in matplot
    display_plots(df, end_times, boundary_pred)
    
if __name__ == "__main__":
    main(NUM_RUNS) # iterations
