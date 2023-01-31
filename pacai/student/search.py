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
    fringe = stack.Stack()
    fringe.push((problem.startingState(), []))

    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        path = node[1]
        # print('curr node = %s' % str(node))
        if problem.isGoal(state):
            # print('found goal: %s' % str(node))
            # print('Visit History: %s' % str(problem.getVisitHistory()))
            # print('Expanded Count: %s' % str(problem.getExpandedCount()))
            return path
        for child in problem.successorStates(state):
            child_state = child[0]
            action = child[1]
            if child_state not in problem.getVisitHistory():
                # print('pushing child to fringe: %s' % str(child[0]))
                child_path = path.copy()
                child_path.append(action)
                fringe.push((child_state, child_path))

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

    fringe = queue.Queue()
    fringe.push((problem.startingState(), []))

    if problem.isGoal(problem.startingState()):
        # print('found goal: %s' % str(node))
        return []

    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        path = node[1]
        # print('curr node = %s' % str(node))
        for child in problem.successorStates(state):
            child_state = child[0]
            action = child[1]
            child_path = path.copy()
            child_path.append(action)

            if problem.isGoal(child_state):
                return child_path
            if child_state not in problem.getVisitHistory():
                # print('pushing child to fringe: %s' % str(child[0]))
                fringe.push((child_state, child_path))

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

    fringe = priorityQueue.PriorityQueue()
    fringe.push((problem.startingState(), []), 0)

    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        path = node[1]

        if problem.isGoal(state):
            return path

        for child in problem.successorStates(state):
            child_state = child[0]
            action = child[1]
            child_path = path.copy()
            child_path.append(action)

            if child_state not in problem.getVisitHistory() or child_path < path:
                child_path = path.copy()
                child_path.append(action)
                path_cost = problem.actionsCost(child_path)
                print(path_cost)
                fringe.push((child_state, child_path), path_cost)

    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    fringe = priorityQueue.PriorityQueue()
    fringe.push((problem.startingState(), []), 0)

    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        path = node[1]

        if problem.isGoal(state):
            return path

        for child in problem.successorStates(state):
            child_state = child[0]
            action = child[1]
            child_path = path.copy()
            child_path.append(action)

            if child_state not in problem.getVisitHistory() or child_path < path:
                child_path = path.copy()
                child_path.append(action)
                path_cost = problem.actionsCost(child_path) + heuristic(child_state, problem)
                fringe.push((child_state, child_path), path_cost)
    raise NotImplementedError()
