# from pacai.util.priorityQueue import PriorityQueue
from pacai.util.queue import Queue
from pacai.agents.capture.dummy import DummyAgent
from pacai.agents.capture.capture import CaptureAgent
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
    secondAgent = OffensiveAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

from pacai.agents.capture.reflex import ReflexCaptureAgent

class OffensiveAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
    
    def chooseAction(self, gameState):
        # print(self.getTeam(gameState))
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
        if (len(foodList) > 0):
            myPos = gameState.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        return features


    def getWeights(self, gameState):
        return {
            'successorScore': 100,
            'distanceToFood': -1
        }
