import numpy as np
import random

# Parameters (d=50,100 and N=2,4 )
d = 50  # Number of islands
N = 2  # Fixed island size
b, c = 2, 1  # Payoff matrix parameters
m = 0.1  # Migration rate
alpha_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # Different alpha values
num_simulations = 100000  # Number of simulations

# Function to calculate payoff based on types in the island
def calculate_payoff(individual_type, n_C, n_D, b, c):
    if individual_type == 'C':
        return n_C * (b - c) + n_D * (-c)
    else:
        return n_C * b

# Function to run a single simulation for a given alpha
def run_simulation(alpha):
    # Initialize demes
    demes = [['D', 'D'] for _ in range(d)]  # All islands start with 2 type D individuals

    # Set one deme with a single C and the rest D
    start_deme = random.choice(range(d))
    demes[start_deme][0] = 'C'

    # Simulation loop until fixation
    while True:
        # Check for fixation condition
        counts = [individual for deme in demes for individual in deme]
        if all(ind == 'C' for ind in counts) or all(ind == 'D' for ind in counts):
            return counts[0]  # Returns type that fixed ('C' or 'D')

        # Randomly select an island
        island_index = random.randint(0, d - 1)
        deme = demes[island_index]

        # Calculate fitness of each individual in the deme
        n_C = deme.count('C')
        n_D = deme.count('D')
        fitness = []
        for individual in deme:
            payoff = calculate_payoff(individual, n_C, n_D, b, c)
            fitness.append(1 + payoff / (N * d))

        # Select an individual to reproduce based on fitness
        parent = random.choices(deme, weights=fitness, k=1)[0]
        offspring = parent  # Offspring inherits type of parent

        # Determine if offspring migrates
        if offspring == 'D':
            migrates = random.random() < m
        else:  # type C
            migrates = random.random() < m + (alpha * n_D) / (N^2 * d)

        if migrates:
            # Migrate to another random island and replace an individual
            target_island = random.choice([i for i in range(d) if i != island_index])
            target_deme = demes[target_island]
            replace_index = random.randint(0, N - 1)
            target_deme[replace_index] = offspring
        else:
            # Stay in the current island and replace a random individual
            replace_index = random.randint(0, N - 1)
            deme[replace_index] = offspring

# Run simulations for each alpha value and store results in a table
with open("simulation_results.txt", "w") as file:
    file.write("Alpha\tFixation_C\tFixation_D\n")
    for alpha in alpha_values:
        fixation_counts = {'C': 0, 'D': 0}
        for _ in range(num_simulations):
            result = run_simulation(alpha)
            fixation_counts[result] += 1
        
        # Print results immediately after each alpha is processed
        print(f"Alpha: {alpha}, Fixation_C: {fixation_counts['C']}, Fixation_D: {fixation_counts['D']}")
        
        # Write results to file
        file.write(f"{alpha}\t{fixation_counts['C']}\t{fixation_counts['D']}\n")

print("Simulation complete. Results saved to 'simulation_results.txt'")
