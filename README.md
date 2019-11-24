# genetic-TSP
Genetic algorithm approach to the Traveling Salesman Problem

An algorithm that uses genetic algorithms to determine the shortest distance between a list of coordinates.
Coordinates are set in an array in the coords variable.

Parameters include the following:
- census_default: the default size of the population.
- choice_weight: the relative weight that determines a path's likeliness for breeding selection based on it's length compared to other path lengths. A higher weight makes a shorter path more likely to be selected for breeding and a longer path less likely to be selected.
- mutate-chance: the probability that a random alteration in a path will be made
- loops: the amount of times the population goes through breeding/dying cycles.
