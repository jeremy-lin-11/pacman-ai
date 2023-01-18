"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util import stack

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    
    Start: (5, 5)
    Is the start a goal?: False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    ```
    """
    frontier = stack.Stack()
    frontier.push(problem.startingState())

    while not frontier.isEmpty():
        node = frontier.pop()
        print(problem.isGoal(problem.successorStates(node)[0]))




    

    raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
