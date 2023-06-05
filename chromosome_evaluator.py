# A way to evaluate RuleAgentChromosome
# The objective of this class is that it could easily be extended 
# into a genentic algorithm engine to improve chromosomes.
# M. Fairbank. October 2021.
import sys
from hanabi_learning_environment import rl_env
from myagent import MyAgent
import os, contextlib
import platform
import random 
import numpy as np


def run(environment, num_episodes, num_players, chromosome, verbose=False):
    """Run episodes."""
    game_scores = []
    for episode in range(num_episodes):
        observations = environment.reset()
        agents = [MyAgent({'players': num_players},chromosome) for _ in range(num_players)]
        done = False
        episode_reward = 0
        while not done:
            for agent_id, agent in enumerate(agents):
                observation = observations['player_observations'][agent_id]
                action = agent.act(observation)
                if observation['current_player'] == agent_id:
                    assert action is not None   
                    current_player_action = action
                    if verbose:
                        print("Player",agent_id,"to play")
                        print("Player",agent_id,"View of cards",observation["observed_hands"])
                        print("Fireworks",observation["fireworks"])
                        print("Player",agent_id,"chose action",action)
                        print()
                else:
                    assert action is None
            # Make an environment step.
            observations, reward, done, unused_info = environment.step(current_player_action)
            if reward<0:
                reward=0 # we're changing the rules so that losing all lives does not result in the score being zeroed.
            episode_reward += reward
            
        if verbose:
            print("Game over.  Fireworks",observation["fireworks"],"Score=",episode_reward)
        game_scores.append(episode_reward)
    return sum(game_scores)/len(game_scores)

if __name__=="__main__":
    num_players=4
    environment=rl_env.make('Hanabi-Full', num_players=num_players)
    if platform.system()=="Windows":
        # We're on a Windows OS.
        # A temporary work-around to fix the problem that it seems on Windows, the random seed always shuffles the deck exactly the same way.
        import random
        for i in range(random.randint(1,100)):
            observations = environment.reset()

    population = [random.sample(range(16), 16) for _ in range(100)] # generate a population of 100 chromosomes with random values between 0 and 15
    best_fitness = 0
    best_chromosome = None

    for generation in range(300):
        tournament_participants = random.sample(population, 10) # select 10 random chromosomes from the population for the tournament
        tournament_winner = max(tournament_participants, key=lambda chromosome: run(environment, 60, num_players, chromosome)) # select the winner of the tournament based on its fitness

        mutated_chromosome = tournament_winner.copy()
        mutation_point = random.randint(0, len(mutated_chromosome) - 1)
        mutated_chromosome[mutation_point] = (mutated_chromosome[mutation_point] + random.randint(1, 15)) % 16

        if run(environment, 60, num_players, mutated_chromosome) > best_fitness:
            best_fitness = run(environment, 60, num_players, mutated_chromosome)
            best_chromosome = mutated_chromosome
        else:
            population[population.index(tournament_winner)] = mutated_chromosome

        if 15 not in best_chromosome:
             best_chromosome.append(15)

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                fitness=run(environment, 60, num_players, best_chromosome)

        print("Generation", generation, "Fitness", fitness, "BestFitness", best_fitness)
        print("Best chromosome", best_chromosome)

    # chromosome = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # best_fitness = 0
    # chromosome_test = chromosome.copy()

    # for generation in range(1000):
    #     start = random.randint(0,len(chromosome_test)-1)
    #     chromosome_test[start]=(chromosome_test[start] + random.randint(0,15)) % 16#step

    #     if 15 not in chromosome_test:
    #         chromosome_test.append(15)

    #     if len(chromosome_test) > 16:
    #         chromosome_test = chromosome_test[-16:]

    #     with open(os.devnull, 'w') as devnull:
    #         with contextlib.redirect_stdout(devnull):
    #             fitness=run(environment, 100, num_players, chromosome_test)

    #     if fitness > best_fitness:
    #         chromosome, best_fitness = chromosome_test, fitness

    #     print("Generation",generation, "Fitness", fitness, "BestFitness", best_fitness)
    #     print("Best chromosome", chromosome_test)

