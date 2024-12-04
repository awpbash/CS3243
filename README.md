# CS3243: Introduction to Artificial Intelligence

This repository contains learning materials for CS3243 for Academic Year 24/25 Semester 1.

## Topics include:
1) Introduction to AI
2) Types of AI agents
3) Uninformed Search
4) Informed Search
5) Local Search and Goal Search
6) Constraint Satisfaction Problems
7) Adversarial Search
8) Logical Agents and Knowledge Base
9) Bayes' Theorem

## Materials
1) Lecture notes
2) Tutorials
3) Projects
4) Past year exam papers

## Introduction to AI
This chapter gives a brief introduction to the types of AI problem environments. This includes:

| Property                     | CS3243 | Notes                          |
|------------------------------|--------|--------------------------------|
| Fully / Partially Observable | Both   | Latter in [Logical Agents] |
| Deterministic / Stochastic   | Both   | Latter in [Bayesian Networks] |
| Episodic / Sequential        | Both   |                                |
| Discrete / Continuous        | Both   | Mostly discrete               |
| Single / Multi-agent         | Both   | Latter in [Adversarial Search] |
| Known / Unknown              | Known  |                                |
| Static / Dynamic             | Static |                                |

![image](https://github.com/user-attachments/assets/3e7ab1b5-ad8c-45e2-b898-01a89e16656c)

## Uninformed Search
This chapter discusses the types of frontiers and searching algorithms on an uninformed searching problem such as shortest path problems. We also compare the types of graph implementations and compare their performance against Tree search algorithms.

![image](https://github.com/user-attachments/assets/9e532e53-dfb7-482f-8c54-9b5b0e95687e)

## Informed Search
Given that we have substantial information on the approximate distance to the goal, this chapter will introduce how we can utilize this information to help guide us to our goal using more efficient searching algorithms like Greedy Best First Search and A* algorithm. Additionally, it delves into crafting admissible and consistent heuristics while quantitatively evaluating the performance of dominant heuristics.

![image](https://github.com/user-attachments/assets/1a306db6-05ef-44fc-9981-06413abd0bbf)

## Local Search and Goal Search
Learn about valid goal states and how we can use various methods to help us find satisfactory solutions and hopefully optimal solutions. Algorithms include K-beam search, Stochastic hill-climbing, and random restarts.

![image](https://github.com/user-attachments/assets/831be8db-0e18-4717-a49e-c7b91960854a)

## Constraint Satisfaction Problems
Learn how to formulate constraint problems and apply heuristics to effectively reduce the search space, including techniques like Minimum Remaining Value (MRV), Degree Heuristic, Least-Constraining Value (LCV), Forward Checking, and the AC3 algorithm.

![image](https://github.com/user-attachments/assets/0301d255-ac81-4541-a00d-b9786088aeba)

## Adversarial Search
Learn how to implement algorithms for multi-agent problems like tic-tac-toe and chess. Learn how to formulate and represent this as a tree search problem, the complexity of these games, and ab-pruning to help speed up our search process. 

![image](https://github.com/user-attachments/assets/aecb351e-3bba-4b00-9caa-18b66948792c)

## Logical agents and knowledge base
This chapter focuses on representing information in a knowledge base and reasoning with it effectively. We learn about truth table enumeration, resolution for proof by contradiction, and the concepts of entailment to determine logical implications. The chapter also introduces the soundness and completeness of algorithms, ensuring they derive valid and complete conclusions.

## Bayesian Network
This chapter introduces Bayes' Theorem, a fundamental principle for reasoning under uncertainty, which allows us to compute posterior probabilities using prior knowledge and observed evidence. Building on this, Bayesian Networks are explored as graphical models that represent probabilistic relationships between variables, enabling efficient computation and reasoning in complex domains. Together, these tools provide a powerful framework for probabilistic inference and decision-making.

![image](https://github.com/user-attachments/assets/62a47aa0-f14c-456c-81b4-574aa8a66e92)


