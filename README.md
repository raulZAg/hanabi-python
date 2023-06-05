# Hanabi agent - "myagent"

This repository contains a Python agent for the cooperative card game Hanabi, developed using the Hanabi Python framework by Dr. Michael Fairbank. The agent, named "myagent", uses a combination of genetic algorithms and a list of rules to make decisions during gameplay.

## Project Overview

Hanabi is a cooperative card game where players, who can see other players' cards but not their own, must play cards in the correct order to win the game. In this project, I've developed a bot that can play Hanabi independently.

The logic of "myagent" is based on a combination of a list of rules that are strategies to play the game and genetic algorithms that uses a chromosome to pick the best set of rules out of the list. The bot uses a series of decision rules, based on the current state of the game, to make its decisions.

## Getting Started

Here are the steps to run "myagent" in a Hanabi game:

Make sure Python is installed on your system.
Clone this repository to your local machine.
Navigate to the directory where the bot file (myagent.py) is located.

To run the agent we just need to run myagent.py. In it, the optimal chromosome is already selected.

## File Overview

myagent.py: This is the main agent file. It contains the decision rules for the bot to play Hanabi.

The chromosome_evaluator.py file contains the genetic algorithm that was used to obtain the optimal chromosome.

## Genetic algorithms
The bot utilizes genetic algorithms in its decision-making process, with each decision represented as a chromosome in the genetic algorithm. These chromosomes contain information about various aspects of the game, such as current hand state, the history of plays, and remaining cards. The bot evaluates these chromosomes based on a fitness function, which is designed to maximize the probability of winning the game. This process of selection, crossover, and mutation allows the bot to continuously learn and adapt its strategy over time, optimizing its game play decisions with each generation.
