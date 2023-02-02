"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util import stack, queue, priorityQueue

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
    ```
    tiny:
        path cost 10
        expanded 15
    medium:
        path cost 130
        expanded 146
    big:
        path cost 210
        expanded 390
    """
    if problem.isGoal(problem.startingState()):
        return []

    fringe = stack.Stack()
    fringe.push((problem.startingState(), []))
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoal(state):
            return path
        for child, action, cost in problem.successorStates(state):
            if child not in visited:
                # print('pushing child to fringe: %s' % str(child[0]))
                fringe.push((child, path + [action]))
                visited.add(child)

    raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 77]

    medium:
        path cost 68
        expanded 273
    big:
        path cost 210
        expanded 617
    """
    if problem.isGoal(problem.startingState()):
        return []

    fringe = queue.Queue()
    fringe.push((problem.startingState(), []))
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        for child, action, cost in problem.successorStates(state):
            if problem.isGoal(child):
                return path + [action]
            if child not in visited:
                fringe.push((child, path + [action]))
                visited.add(child)

    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first. p 73
    meddot:
        nodes expanded: 190
        total cost: 1
    medmaze:
        nodes expanded: 274
        total cost: 68
    medscary:
        nodes expanded: 108
        total cost: 68719479864
    """
    if problem.isGoal(problem.startingState()):
        return []

    fringe = priorityQueue.PriorityQueue()
    fringe.push((problem.startingState(), []), 0)
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoal(state):
            return path
        for child, action, cost in problem.successorStates(state):
            if child not in visited:
                fringe.push((child, path + [action]),
                            problem.actionsCost(path + [action]))
                visited.add(child)

    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    if problem.isGoal(problem.startingState()):
        return []

    fringe = priorityQueue.PriorityQueue()
    fringe.push((problem.startingState(), []), 0)
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoal(state):
            return path
        for child, action, cost in problem.successorStates(state):
            if child not in visited:
                fringe.push((child, path + [action]),
                            problem.actionsCost(path + [action]) + heuristic(child, problem))
                visited.add(child)

    raise NotImplementedError()
