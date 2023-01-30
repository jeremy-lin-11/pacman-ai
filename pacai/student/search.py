"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util import stack, queue, priorityQueue

def getActionPath(problem, node, parent_dict):
    action_list = []
    while node != problem.startingState():
        node, action = parent_dict[node][0], parent_dict[node][1]
        # print(node, action)
        action_list.insert(0, action)
    # print(action_list)
    # print('Solution length = %s' % str(len(action_list)))
    return action_list

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
    fringe.push(problem.startingState())
    parent_dict = {}

    while not fringe.isEmpty():
        node = fringe.pop()
        # print('curr node = %s' % str(node))
        if problem.isGoal(node):
            # print('found goal: %s' % str(node))
            # print('Visit History: %s' % str(problem.getVisitHistory()))
            # print('Expanded Count: %s' % str(problem.getExpandedCount()))
            return getActionPath(problem, node, parent_dict)

        for child in problem.successorStates(node):
            if child[0] not in problem.getVisitHistory():
                # print('pushing child to fringe: %s' % str(child[0]))
                fringe.push(child[0])
                parent_dict[child[0]] = tuple([node, child[1]])

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
    fringe.push(problem.startingState())
    parent_dict = {}

    if problem.isGoal(problem.startingState()):
        # print('found goal: %s' % str(node))
        return getActionPath(problem, problem.startingState(), parent_dict)

    while not fringe.isEmpty():
        node = fringe.pop()
        # print('curr node = %s' % str(node))
        for child in problem.successorStates(node):
            # state = child[0]
            # action = child[1]
            if problem.isGoal(child[0]):
                parent_dict[child[0]] = tuple([node, child[1]])
                return getActionPath(problem, child[0], parent_dict)
            if child[0] not in problem.getVisitHistory():
                # print('pushing child to fringe: %s' % str(child[0]))
                fringe.push(child[0])
                parent_dict[child[0]] = tuple([node, child[1]])

    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first. p 73
    """

    fringe = priorityQueue.PriorityQueue()
    fringe.push(problem.startingState())
    parent_dict = {}
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
