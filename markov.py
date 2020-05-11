from random import random
import time
from os import system
import numpy as np
from scipy.linalg import eig
# this is the progress bar, pip install <tqdm> if there are any issues
from tqdm import tqdm

def chain_size():
    """
    Finds out from the user how many nodes there are in the Markov chain.

    Returns: nodes (int) - The number of nodes in the chain.
    """
    while(True):
        try:
            nodes = int(input("How many nodes are there?\n"))
            break
        except ValueError:
            print("You must enter a valid integer, please try again.")
    print("There are " + str(nodes) + " nodes.")
    return nodes

def create_matrices(nodes):
    """
    Creates the transition matrix and the position list.
    Parameters: nodes (int) - The number of nodes in the chain.
    Returns: t_matrix (2d list) - The transition matrix of the Markov chain.
             p_list (list) - List of the populations on each node
    """
    # t_matrix is the transition matrix
    # creates an n*n list where n is the value of nodes
    t_matrix = [x[:] for x in [[0] * nodes] * nodes]
    p_list = [0 for i in range(nodes)] # creates a population list for the population of each node

    return t_matrix, p_list

def fill_t_matrix(t_matrix, nodes):
    """
    Allows the user to fill in the transition matrix with whatever values they want.
    Parameters: t_matrix (2d list) - The current empty transition matrix.
                nodes (int) - The number of nodes in the chain.
    Returns: t_matrix (2d list) - The updated transition matrix with user-inputted values.
    """
    print("You must fill in the transition matrix.")
    for i in range(len(t_matrix)):
        for j in range(len(t_matrix[i])):
            while(True):
                try:
                    t_matrix[i][j] = float(input("Value for position [" + str(i) + ", " + str(j) + "]: "))
                    break
                except ValueError:
                    print("You must enter a floating point value, Try again.")
    system('cls')
    print("here is the transition matrix you have given.")
    for row in t_matrix:
        print("\t" + str(row))
    cont = input("If it is incorrect, type 'n' to re-enter the values.\nAny other key will allow you to continue. ")
    if(cont == "n" or cont == "N"):
        fill_t_matrix([x[:] for x in [[0] * nodes] * nodes], nodes) # sends a new empty list to this function
    return t_matrix

def fill_p_list(p_list, nodes):
    """
    Allows the user to fill in the population list with the starting populations for each node.
    Parameters: p_list (list) - An empty list that is the length of the number of nodes in the chain.
                nodes (int) - The number of nodes in the chain.
    Returns: p_list (list) - The updated population list with user-inputted values.
    """
    print("\nYou must specify the starting population for each node.")
    for i in range(nodes):
        while(True):
            try:
                p_list[i] = int(input("Population of node " + str(i + 1) + ": "))
                break
            except ValueError:
                print("You must input a positive integer, try again.")
    print("here are the starting populations you have given.")
    for i in range(nodes):
        print("Node " + str(i+1) + ": " + str(p_list[i]))
    cont = input("If any are incorrect, type 'n' to re-enter the values.\nAny other key will allow you to continue. ")
    if(cont == "n" or cont == "N"):
        fill_p_list([0 for i in range(nodes)], nodes) # sends a new empty list to this function
    return p_list

def steady_state(t_matrix, nodes):
    """
    Finds the steady state of the Markov chain, if a steady state exists. If there is no steady state,
    it will attempt to at least find steady state proportions.
    Parameters: t_matrix (2d list) - The transition matrix for the Markov chain.
                nodes - The number of nodes in the Markov chain.
    Returns: state_vector (list) - a list of the steady state values. This is usually what is returned.
             final_ratio (list) - a list of steady state proportions. This is only returned if there is not a true steady state.
    """
    state = 0
    for i in range(nodes):
        state += t_matrix[0][i]
    t_matrix = np.matrix(t_matrix)   
    # the next 3 lines were found on stack overflow to calculate the steady state
    # source: https://stackoverflow.com/questions/31791728/python-code-explanation-for-stationary-distribution-of-a-markov-chain
    S, U = eig(t_matrix.T)
    state_vector = np.array(U[:, np.where(np.abs(S - state) < 1e-8)[0][0]].flat)
    state_vector = state_vector / np.sum(state_vector)
    # if there is a steady state, it is returned
    if(state == 1):
        for y in range(len(state_vector)):
            state_vector[y] = round(state_vector[y].real, 2)
        return state_vector
    # if no steady state is present, the steady state proportions will be found
    else:
        big = -1000.0
        for num in state_vector:
            if(num > big):
                big = num
        state_vector = np.array(state_vector)
        state_ratio = state_vector/big
        final_ratio = []
        for x in range(len(state_ratio)):
            final_ratio.append(round(state_ratio[x].real, 2))
        return final_ratio   

def simulate(t_matrix, p_list):
    """
    Simulates the Markov chain and its changes over a given number of steps.
    Parameters: t_matrix (2d list) - The transition matrix for the Markov chain.
    Returns: p_list (list) - The population list after the simulation is over.
    """
    new_p_list = [0 for i in range(len(p_list))]
    steps = int(input("\nHow many steps would you like to take? "))
    # loops for however many steps are specified
    # tqdm in the for loop adds a progress bar
    for i in tqdm(range(steps)):
        # loops through p_list
        for j in range(len(p_list)):          
            # loops through the population of the current p_list element
            for k in range(p_list[j]):
                chance = random() # random number that will decide where the node moves
                start = 0
                # loops through each column in the t_matrix
                for l in range(len(t_matrix)):
                    if(chance > start and chance < (t_matrix[j][l] + start)):
                        new_p_list[l] += 1
                        break
                    start += t_matrix[j][l]
        p_list = new_p_list
        new_p_list = [0 for i in range(len(p_list))]
        #for reference 
        # i = current step of simulation
        # j = current position in p_list
        # k = current position of specific population value in p_list
        # l = current column of t_matrix
    return p_list

def simulate_steps(t_matrix, p_list):
    """
    Simulates the Markov chain and its changes over a given number of steps.
    This version of the function is incremental and lets you step through it at
    your own pace.
    Parameters: t_matrix (2d list) - The transition matrix for the Markov chain.
    Returns: p_list (list) - The population list after the simulation is over.
    """
    new_p_list = [0 for z in range(len(p_list))]
    steps = int(input("\nHow many steps would you like to take? "))
    print("You will be shown the current population after each step. Press enter to continue, or type 'n' to quit.")
    # loops for however many steps are specified
    # tqdm in the for loop adds a progress bar
    for i in (range(steps)):
        # loops through p_list
        for j in range(len(p_list)):          
            # loops through the population of the current p_list element
            for k in range(p_list[j]):
                chance = random() # random number that will decide where the node moves
                start = 0
                # loops through each column in the t_matrix
                for l in range(len(t_matrix)):
                    if(chance > start and chance < (t_matrix[j][l] + start)):
                        new_p_list[l] += 1
                        break
                    start += t_matrix[j][l]
        p_list = new_p_list
        new_p_list = [0 for y in range(len(p_list))]
        nodes_pop = ""
        for x in range(len(p_list)):
            nodes_pop += ("Node " + str(x+1) + ": " + str(p_list[x]) + "   ")    
        user_in = input("step " + str(i+1) + " node populations =>  " + str(nodes_pop))
        if(user_in == 'n' or user_in == "N"):
            return p_list
        #for reference 
        # i = current step of simulation
        # j = current position in p_list
        # k = current position of specific population value in p_list
        # l = current column of t_matrix
    return p_list

if __name__ == "__main__":
    nodes = chain_size()
    t_matrix, p_list = create_matrices(nodes)
    t_matrix = fill_t_matrix(t_matrix, nodes)
    p_list = fill_p_list(p_list, nodes)
    p_list = simulate(t_matrix, p_list)
    steady = steady = steady_state(t_matrix, nodes)

    print("\nThe population of each node after the simulation is:\n\t" + str(p_list) + "\n")
    print("The calculated steady state values are: ")
    for i in range(len(steady)):
        print("\tNode " + str(i+1) + ":\t" + str(steady[i]))







