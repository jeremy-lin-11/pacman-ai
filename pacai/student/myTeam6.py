from pacai.agents.capture.dummy import DummyAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
import random
import time
# from pacai.util.priorityQueue import PriorityQueue
# from pacai.util.queue import Queue
# from pacai.util import util
# import logging
# from collections import Counter
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
    
    def chooseAction(self, gameState):
        #minmax()
        #method that caches distances to the food
        # Returns max value from future predictions to make ideal action for pacman
        def maxVal(state, agentIndex, currDepth):
            currDepth += 1
            # Checks if in terminal state
            if state.isLose() or state.isWin() or currDepth == 2:
                return self.evaluate(state)
            v = float("-inf")
            # Loops through possible future actions and saves max value prediction
            for direction in state.getLegalActions(agentIndex):
                # Checks and skips Stop command
                if direction == "Stop":
                    continue
                if agentIndex + 1 < state.getNumAgents():
                    v = max(v, minVal(state.generateSuccessor(agentIndex, direction), agentIndex + 1, currDepth))
                else:
                    v = max(v, minVal(state.generateSuccessor(agentIndex, direction), 0, currDepth))
            return v

        # Returns min value from future predictions to make ideal action for ghosts
        def minVal(state, agentIndex, currDepth):
            # Checks if in terminal state
            if state.isLose() or state.isWin() or currDepth == 2:
                return self.evaluate(state)
            v = float("inf")
            # Loops through possible future actions and saves mix value prediction
            for direction in state.getLegalActions(agentIndex):
                # Checks and skips Stop command
                if direction == "Stop":
                    continue
                # Checks if next agent if not pacman
                if agentIndex + 1 < state.getNumAgents():
                    v = min(v, maxVal(state.generateSuccessor(agentIndex, direction),
                                    agentIndex + 1, currDepth))
                else:
                    v = min(v, maxVal(state.generateSuccessor(agentIndex, direction), 0, currDepth))
            return v

        # Saves highest maximum score and assoicated move for pacman
        action, maxScore = "West", float("-inf")
        # Loops through the actions that pacman can take at the current board
        for direction in gameState.getLegalActions(self.index):
            # Checks and skips Stop command
            if direction == "Stop":
                continue
            successorScore = float("-inf")
            if self.index + 1 < gameState.getNumAgents():    
                successorScore = minVal(gameState.generateSuccessor(self.index, direction), self.index + 1, 0)
            else:
                successorScore = minVal(gameState.generateSuccessor(self.index, direction), 0, 0)
            # Checks if current action results in a larger score than max score
            if maxScore < successorScore:
                maxScore = successorScore
                action = direction
        return action

    def evaluate(self, gameState):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState)
        weights = self.getWeights(gameState)
        stateEval = sum(features[feature] * weights[feature] for feature in features)

        return stateEval

    def getFeatures(self, gameState):
        features = {}
        #myPos = gameState.getAgentPosition(self.index)
        #successor = self.getSuccessor(gameState, action)
        #myState = successor.getAgentState(self.index)
        features['successorScore'] = self.getScore(gameState)

        # Compute distance to the nearest food.
        foodList = self.getFood(gameState).asList()

        # This should always be True, but better safe than sorry.
        myPos = gameState.getAgentState(self.index).getPosition()
        if (len(foodList) > 0):
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        return features

    def getWeights(self, gameState):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
        }

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

        maxProb = max(self.defenderList[x] for x in self.defenderList.keys())
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

        defendingFoodList = self.getFoodYouAreDefending(gameState).asList()
        if self.previousFood and len(self.previousFood) != len(defendingFoodList):
            self.DefendingProbability(gameState)

        CurrentPosition = gameState.getAgentPosition(self.index)
        if CurrentPosition == self.target:
            self.target = None

        opponentsState = []
        for i in self.getOpponents(gameState):
            opponentsState.append(gameState.getAgentState(i))

        visible = [opponent for opponent in opponentsState if
                   opponent.isPacman and opponent.getPosition() is not None]

        if len(visible) > 0:
            positions = [invader.getPosition() for invader in visible]
            minDis, self.target = min(
                [(self.getMazeDistance(CurrentPosition, position), position) for
                 position in positions])

        elif self.previousFood is not None:
            eaten = [food for food in self.previousFood if
                     food not in self.getFoodYouAreDefending(gameState).asList()]
            if len(eaten) > 0:
                self.target = eaten.pop()

        self.previousFood = self.getFoodYouAreDefending(gameState).asList()

        if self.target is None and len(self.getFoodYouAreDefending(gameState).asList()) <= 4:
            food = self.getFoodYouAreDefending(
                gameState).asList() + self.getCapsulesYouAreDefending(gameState)
            self.target = random.choice(food)

        elif self.target is None:
            self.target = self.selectPatrolTarget()

        actions = gameState.getLegalActions(self.index)

        feasible = [a for a in actions if not a == Directions.STOP
                    and not gameState.generateSuccessor(self.index,
                                                        a).getAgentState(self.index).isPacman()]
        fvalues = [self.getMazeDistance(
            gameState.generateSuccessor(self.index, a).getAgentPosition(
                self.index), self.target) for a in actions if not a == Directions.STOP
            and not gameState.generateSuccessor(self.index, a).getAgentState(self.index).isPacman()]

        # Randomly chooses between ties.

        best = min(fvalues)
        ties = list(filter(lambda x: x[0] == best, zip(fvalues, feasible)))

        # print 'eval time for defender agent %d: %.4f' % (self.index, time.time() - start)
        return random.choice(ties)[1]
