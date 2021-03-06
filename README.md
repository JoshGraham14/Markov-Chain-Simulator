# Markov-Chain-Simulator
A python program that can simulate Markov chains. You input the transition matrix, initial populations, and it can simulate however many steps you want.

IMPORTANT: please view the raw version of this read me to see the proper formatting, which is necessary.

# Format for transition matrices
There are generally two ways that transition matrices are created. The first way is where the columns represent the starting position and the rows represent the ending position. The second way, which is the way that this code works is where the rows are the starting position and the columns are the ending position. Please make sure that the transition matrix you use is formatted this way.

Here is an example to illustrate this:
       TO   TO
FROM [0.3  0.7]       Given this 2 node example, I'll walk you through what the transition matrix means. The 0.3 in the top left is in the 
FROM [0.6  0.4]       first column and first row. This means that the transition FROM node 1 TO node 1 has a probability of 0.3. Now we'll 
                      take a look at the 0.6 below it. This 0.6 value means that the transition is FROM node 2 TO node 1, with a
                      probability of 0.6.

When you are asked to fill in the transition matrix, you will first be asked for the value of position [1,1]. Indexing begins at 1 for this, so that is the top left corner of the matrix. Think of the first value as the FROM node and the second value as the TO node. So for [1,1] it is asking you for the probability FROM node 1 TO node 1.
