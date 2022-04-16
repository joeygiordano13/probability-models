# models.py
import sys
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt

WIN = 1
LOSE = 0
MAX_STEPS = 1000

def sim(p, start, goal, df, iter):
    """
    Run main simulation. 
    Args:
        p: (int) probability of success for each step
        start: (int) how much money you start with
        goal: (int) the upper bound of cash where you stop
        df: (pd.DataFrame) dataframe to append cash walk timesteps
        iter: (int) iteration of sim
    Returns: 
        time_to_end: (int) number of steps to reach boundary condition
        success: (bool) reached upper bound, or lost all money
    """
    print(f"Running gambling simulation...")

    t = 0 # init step
    steps = np.array()
    cash = start
    # simulation loop
    while (t < MAX_STEPS):
        rand = random.random()
        state = WIN if rand < p else LOSE # determine round result
        cash += 1 if state is WIN else -1 # update cash
        steps.append(cash)

        # end simulation condition
        if cash >= goal or cash <= 0:
            df[f'run-{iter}'] = steps.tolist()
            return (t, WIN) if cash > 0 else (t, LOSE) 

def display(df):
    """
    Plots a series of columns in one graph
    Args:
        df: (pd.DataFrame) dataframe with all the cash walks you want to plot
    """
    print(f"Plotting cash walks...")

    for column in df.iteritems():   #plotting all the cash walks
        plt.plot(df[column])
        
    plt.title('Cash Walks') #the title of the plot
    plt.xlabel('Step')  #the x axis label
    plt.ylabel('Cash Amount')   #the y axis label
    plt.legend('Walk #' + num for num in range(df.shape[1]))    #the legend of the plot



def main(numiter):
    print(f"In main, calling gambling sim {numiter} times")
    p = input("Probability of success per round")
    start = input("Starting money")
    goal = input("Goal money")
   
    end_times = []
    end_states = []

    df = pd.DataFrame()
    
    # Running simulation N times
    for i in range(numiter): 
        time, state = sim(p, start, goal, df)
        end_times.append(time)
        end_states.append(state)
    # Print output
    for i in range(numiter):
        print(f"Iter {i}: time - {end_times[i]} state - {end_states[i]}")
    # Display output in matplot
    display(df)
    
if __name__ == "__main__":
    main(sys.argv[0]) # iterations
