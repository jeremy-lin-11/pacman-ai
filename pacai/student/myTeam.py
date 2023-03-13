# from pacai.util.priorityQueue import PriorityQueue
from pacai.util.queue import Queue
from pacai.agents.capture.dummy import DummyAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.util import util
from pacai.core.directions import Directions
import logging
import random
import time
from collections import Counter
# import time
def createTeam(firstIndex, secondIndex, isRed,
        first = DummyAgent,
        second = DummyAgent):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = OffensiveAgent
    secondAgent = DefensiveAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class OffensiveAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1
        }

# This is https://github.com/bslqy/Pacman-Capture-the-flag/blob/master/final.py
# class OffensiveAgent(ReflexCaptureAgent):
#     """
#     A reflex agent that seeks food.
#     This agent will give you an idea of what an offensive agent might look like,
#     but it is by no means the best or only way to build an offensive agent.
#     """

#     def __init__(self, index, **kwargs):
#         super().__init__(index)
    
#     def registerInitialState(self, gameState):
#         super().registerInitialState(gameState)
#         # get the deadends of the map
#         self.lastAction=Directions.STOP
#         self.deadEnds = {}
#         # get the feasible position of the map
#         self.feasible = []
#         for i in range(1, gameState.getInitialLayout().height - 1):
#             for j in range(1, gameState.getInitialLayout().width - 1):
#                 if not gameState.hasWall(j, i):
#                     self.feasible.append((j, i))
#         # store the crossroads met in the travel
#         crossRoad = Queue()

#         currentState = gameState
#         # the entrance of the deadend
#         entPos = currentState.getAgentPosition(self.index)
#         entDirection = currentState.getAgentState(self.index).getDirection()
#         actions = currentState.getLegalActions(self.index)
#         actions.remove(Directions.STOP)
#         for a in actions:
#             crossRoad.push((currentState,a))
#         # if there is still some positions unexplored
#         while not crossRoad.isEmpty():
#             # if it is not a crossroad nor a deadend

#             (entState,entDirection) = crossRoad.pop()
#             depth = 0
#             entPos = entState.getAgentState(self.index).getPosition()
#             currentState=entState.generateSuccessor(self.index,entDirection)
#             while True:
#                 # get current position

#                 currentPos = currentState.getAgentState(self.index).getPosition()
#                 # get next actions
#                 actions = currentState.getLegalActions(self.index)
#                 actions.remove(Directions.STOP)
#                 currentDirection = currentState.getAgentState(self.index).getDirection()
#                 if currentPos not in self.feasible:
#                     break
#                 self.feasible.remove(currentPos)
#                 if Directions.REVERSE[currentDirection] in actions:
#                     actions.remove(Directions.REVERSE[currentDirection])

#                 # deadend
#                 if len(actions) == 0:
#                     self.deadEnds[(entPos, entDirection)] = depth + 1
#                     break

#                 # there is only one direction to move
#                 elif len(actions) == 1:
#                     depth = depth + 1
#                     # generate next state
#                     currentState = currentState.generateSuccessor(self.index, actions[0])
#                 # meet crossroad
#                 else:
#                     # get the successors
#                     for a in actions:
#                         crossRoad.push((currentState,a))

#                     break


#         self.distancer.getMazeDistances()
#         if self.red:
#             centralX = int((gameState.getInitialLayout().width - 2) / 2)
#         else:
#             centralX = int(((gameState.getInitialLayout().width - 2) / 2) + 1)
#         self.boundary = []
#         for i in range(1, gameState.getInitialLayout().height - 1):
#             if not gameState.hasWall(centralX, i):
#                 self.boundary.append((centralX, i))

#     def chooseAction(self, gameState):
#         """
#         Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
#         """
#         start = time.time()
#         actions = gameState.getLegalActions(self.index)
#         actions.remove(Directions.STOP)
#         fvalues = []

#         # values = [self.evaluate(gameState, a) for a in actions]
#         # logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))

#         # maxValue = max(values)
#         # bestActions = [a for a, v in zip(actions, values) if v == maxValue]

#         # return random.choice(bestActions)

#         for a in actions:
#             newState = gameState.generateSuccessor(self.index, a)

#             value = self.evaluate(gameState,a)
#             value += self.allSimulation(2, newState, 0.7)
#             if a==Directions.REVERSE[self.lastAction]:
#                 value=value*0.1
#             # print(value,a)
#             fvalues.append(value)
#         """
#             newState = gameState.generateSuccessor(self.index, a)
#             for i in range(30):
#                 value = self.evaluate(gameState,a)
#                 value += self.randomSimulation(10, newState, 0.5)
#             fvalues.append(value)"""
#         best = max(fvalues)
#         ties = filter(lambda x: x[0] == best, zip(fvalues, actions))
#         toPlay = random.choice(list(ties))[1]
#         self.lastAction=toPlay
#         # print(toPlay)
#         # print('eval time for offensive agent %d: %.4f' % (self.index, time.time() - start))
#         return toPlay
    
#     def allSimulation(self, depth, gameState, decay):
#         new_state = gameState
#         if depth == 0:
#             result_list = []
#             actions = new_state.getLegalActions(self.index)
#             actions.remove(Directions.STOP)
#             result_list.append(max(self.evaluate(new_state, a) for a in actions))
#             return max(result_list)

#         # Get valid actions
#         result_list = []
#         actions = new_state.getLegalActions(self.index)
#         actions.remove(Directions.STOP)

#         for a in actions:
#             # Compute new state and update depth

#             next_state = new_state.generateSuccessor(self.index, a)
#             result_list.append(
#                 self.evaluate(new_state, a) + decay * self.allSimulation(depth - 1, next_state, decay))
#         return max(result_list)
    
#     def randomSimulation(self, depth, gameState, decay):
#         """
#         Random simulate some actions for the agent. The actions other agents can take
#         are ignored, or, in other words, we consider their actions is always STOP.
#         The final state from the simulation is evaluated.
#         """
#         currState = gameState
#         value = 0
#         decay_index = 1
#         while depth > 0:

#             # Get valid actions
#             actions = currState.getLegalActions(self.index)
#             # The agent should not stay put in the simulation
#             # actions.remove(Directions.STOP)
#             current_direction = currState.getAgentState(self.index).getDirection()
#             # The agent should not use the reverse direction during simulation

#             reversed_direction = Directions.REVERSE[currState.getAgentState(self.index).getDirection()]
#             if reversed_direction in actions and len(actions) > 1:
#                 actions.remove(reversed_direction)
#             # Randomly chooses a valid action
#             a = random.choice(actions)
#             # Compute new state and update depth
#             value = value + decay ** decay_index * self.evaluate(currState, a)
#             currState = currState.generateSuccessor(self.index, a)
#             depth -= 1
#             decay_index += 1
#         # Evaluate the final simulation state
#         return value

#     def getFeatures(self, gameState, action):
#         features = Counter()
#         successor = self.getSuccessor(gameState, action)
#         # Compute score from successor state
#         features['successorScore'] = self.getScore(successor) - self.getScore(gameState)

#         # Compute distance to the nearest food.
#         foodList = self.getFood(successor).asList()

#         # Get current position of agent
#         myPos = successor.getAgentState(self.index).getPosition()

#         # This should always be True, but better safe than sorry.
#         if (len(foodList) > 0):
#             # Get next position of agent
#             sucPos = successor.getAgentPosition(self.index)
#             minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
#             sucFoodDistance=min([self.getMazeDistance(sucPos, food) for food in foodList])
#             # Subtract successors food distance from minDistance
#             features['distanceToFood'] = minDistance - sucFoodDistance

#         #compute the distance to boundary
#         curBound = min(self.getMazeDistance(myPos, b) for b in self.boundary)
#         sucBound = min(self.getMazeDistance(sucPos, b) for b in self.boundary)
#         # features['towardsBound'] = (curBound - sucBound)

#         # Compute distance to closest ghost
#         features['deadends']=0
#         features['towardsGhost']=0
#         features['towardsBound']=0

#         enemies = [gameState.getAgentState(i) for i in self.getOpponents(successor)]
#         inRange = filter(lambda x: not x.isPacman and x.getPosition() != None and self.getMazeDistance(myPos,x.getPosition())<5 and x.scaredTimer<5, enemies)
#         if len(list(inRange)) > 0:
#             positions = [agent.getPosition() for agent in inRange]
#             closest = min(positions, key=lambda x: self.getMazeDistance(myPos, x))
#             ghostDis = self.getMazeDistance(myPos, closest)
#             sucGhostDis=self.getMazeDistance(sucPos,closest)
#             for agent in inRange:
#                 if agent.getPosition()==closest:
#                     fear=agent
#             #going to deadends

#             if self.deadEnds.has_key((myPos, action)) and self.deadEnds[(myPos, action)] * 2 < ghostDis:
#                 features['deadends'] =1
#             #the ghost is about to eat pacman



#             features['towardsBound'] = (curBound - sucBound)*10
#             runaway=sucGhostDis-ghostDis
#             #you are eaten
#             if fear.scaredTimer<3 and fear.scaredTimer!=0:
#                 if runaway>10:
#                     features['towardsGhost']=100
#                 else:
#                    features['towardsGhost']=-runaway
#             else:
#                 if runaway>10:
#                     features['towardsGhost']=-100
#                 else:
#                    features['towardsGhost']=runaway

#             capsuleList = self.getCapsules(gameState)
#             if len(capsuleList) > 0:
#                 minCapDistance = min([self.getMazeDistance(myPos, c) for c in capsuleList])
#                 sucCapDistance=min([self.getMazeDistance(sucPos, c) for c in capsuleList])

#                 features['towardsCapsule'] = minCapDistance-sucCapDistance
#                 if sucPos in capsuleList:
#                         features['towardsCapsule']=100
#             else:
#                     features['towardsCapsule'] = 0

#         return features

#     def getWeights(self, gameState, action):
#         return {
#             'successorScore': 100,
#             'distanceToFood': 50,
#             'towardsGhost': 500,
#             'towardsCapsule': 500,
#             'towardsBound':5,
#             'deadends': -2000, }

class DefensiveAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
        self.target = None
        self.previousFood = None

    def DefendingProbability(self, gameState):
        """
        This method calculates the minimum distance from our patrol
        points to our pacdots. The inverse of this distance will
        be used as the probability to select the patrol point as
        target.
        """
        foodList = self.getFoodYouAreDefending(gameState).asList()
        total = 0

        # Get the minimum distance from the food to our
        # patrol points.

        for position in self.noWall:
            closestFoodDistance = 99999
            foodList = self.getFoodYouAreDefending(gameState).asList()
            closestFoodDistance = min([self.getMazeDistance(position, food) for food in foodList])

            if closestFoodDistance == 0:
                closestFoodDistance = 1
            self.defenderList[position] = 1.0 / float(closestFoodDistance)
            total += self.defenderList[position]

        # Normalize the value used as probability.
        if total == 0:
            total = 1
        for x in self.defenderList.keys():
            self.defenderList[x] = float(self.defenderList[x]) / float(total)

    def selectPatrolTarget(self):

        maxProb=max(self.defenderList[x] for x in self.defenderList.keys())
        bestTarget = filter(lambda x: self.defenderList[x] == maxProb, self.defenderList.keys())
        return random.choice(bestTarget)

    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)
        self.distancer.getMazeDistances()

        # Compute central positions without walls from map layout.
        # The defender will walk among these positions to defend
        # its territory.

        self.defenderList = {}
        if self.red:
            middle = int((gameState.getInitialLayout().width - 2) / 2)
        else:
            middle = int(((gameState.getInitialLayout().width - 2) / 2) + 1)
        self.noWall = []
        for i in range(1, gameState.getInitialLayout().height - 1):
            if not gameState.hasWall(middle, i):
                self.noWall.append((middle, i))

        self.DefendingProbability(gameState)
    
    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        # actions = gameState.getLegalActions(self.index)

        # start = time.time()
        # values = [self.evaluate(gameState, a) for a in actions]
        # logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))

        # maxValue = max(values)
        # bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        # return random.choice(bestActions)

        defendingFoodList = self.getFoodYouAreDefending(gameState).asList()
        if self.previousFood and len(self.previousFood) != len(defendingFoodList):
            self.DefendingProbability(gameState)

        CurrentPosition = gameState.getAgentPosition(self.index)
        if CurrentPosition == self.target:
            self.target = None

        opponentsState = []
        for i in self.getOpponents(gameState):
            opponentsState.append(gameState.getAgentState(i))

        visible = [opponent for opponent in opponentsState if opponent.isPacman and opponent.getPosition() != None]

        if len(visible) > 0:
            positions = [invader.getPosition() for invader in visible]
            minDis, self.target = min(
                [(self.getMazeDistance(CurrentPosition, position), position) for position in positions])

        elif self.previousFood != None:
            eaten = [food for food in self.previousFood if food not in self.getFoodYouAreDefending(gameState).asList()]
            if len(eaten) > 0:
                self.target = eaten.pop()

        self.previousFood = self.getFoodYouAreDefending(gameState).asList()

        if self.target == None and len(self.getFoodYouAreDefending(gameState).asList()) <= 4:
            food = self.getFoodYouAreDefending(gameState).asList() + self.getCapsulesYouAreDefending(gameState)
            self.target = random.choice(food)

        elif self.target == None:
            self.target = self.selectPatrolTarget()


        actions = gameState.getLegalActions(self.index)


        feasible = [a for a in actions if not a == Directions.STOP
                    and not gameState.generateSuccessor(self.index, a).getAgentState(self.index).isPacman()]
        fvalues = [
            self.getMazeDistance(gameState.generateSuccessor(self.index, a).getAgentPosition(self.index), self.target)
            for a in actions if
            not a == Directions.STOP and not gameState.generateSuccessor(self.index, a).getAgentState(
                self.index).isPacman()]


        # Randomly chooses between ties.

        best = min(fvalues)
        ties = list(filter(lambda x: x[0] == best, zip(fvalues, feasible)))

        # print 'eval time for defender agent %d: %.4f' % (self.index, time.time() - start)
        return random.choice(ties)[1]

    # def getFeatures(self, gameState, action):
    #     features = Counter()

    #     successor = self.getSuccessor(gameState, action)
    #     myState = successor.getAgentState(self.index)
    #     myPos = myState.getPosition()

    #     # Computes whether we're on defense (1) or offense (0).
    #     features['onDefense'] = 1
    #     if (myState.isPacman()):
    #         features['onDefense'] = 0

    #     # Computes distance to invaders we can see.
    #     enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    #     invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
    #     features['numInvaders'] = len(invaders)

    #     if (len(invaders) > 0):
    #         dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
    #         features['invaderDistance'] = min(dists)

    #     if (action == Directions.STOP):
    #         features['stop'] = 1

    #     rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
    #     if (action == rev):
    #         features['reverse'] = 1

    #     return features

    # def getWeights(self, gameState, action):
    #     return {
    #         'numInvaders': -1000,
    #         'onDefense': 100,
    #         'invaderDistance': -10,
    #         'stop': -100,
    #         'reverse': -2
    #     }
