from markov import *
import sys

def menu():
    print("\n---- Markov Chain Simulator ----\n\n" +
            "Please select what you would like to do.")
    while(True):
        menu_in = input("1) Run a Markov chain simulation for a specified number of steps.\n" +
                        "2) Run a Markov chain simulation that you can individually step through.\n" +
                        "3) Quit.\n")
        if(menu_in == "1" or menu_in == "2" or menu_in == "3"):
            if(menu_in == "3"):
                sys.exit()
            return menu_in
        else:
            print("You did not enter a valid option, please select 1, 2, or 3.")
    

def main():
    menu_in = menu()
    while(menu_in == "1" or menu_in =="2"):
        nodes = chain_size()
        t_matrix, p_list = create_matrices(nodes)
        t_matrix = fill_t_matrix(t_matrix, nodes)
        p_list = fill_p_list(p_list, nodes)
        if(menu_in == "2"):
            p_list = simulate_steps(t_matrix, p_list)
        else:
            p_list = simulate(t_matrix, p_list)
        steady = steady_state(t_matrix, nodes)

        print("\nThe population of each node after the simulation is:")
        for i in range(nodes):
            print("\tNode " + str(i+1) + ":\t" + str(p_list[i]))
        print("\nThe calculated steady state values are: ")
        for j in range(len(steady)):
            print("\tNode " + str(j+1) + ":\t" + str(steady[j]))
        menu_in = menu()

main()