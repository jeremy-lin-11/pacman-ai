import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.directions import Directions
from pacai.core.distance import manhattan

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # ghostPos = successorGameState.getGhostPositions()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        score = successorGameState.getScore()
        newFood = successorGameState.getFood()
        newFoodPos = newFood.asList()

        # we die
        if successorGameState.isLose():
            return float("-inf")

        # we win
        if successorGameState.isWin():
            return float("inf")

        # optimistic dist from pacman to all the foods
        foodDist = []
        for food in newFoodPos:
            foodDist.append(manhattan(newPosition, food))

        # Find closest food
        minFood = min(foodDist)

        # minGhost = float("inf")
        for ghost in newGhostStates:
            newGhostPos = ghost.getPosition()
            # minGhost = min(minGhost, manhattan(newPosition, ghost))
            # if we're at a ghost and it's not scared, we lose
            if (newGhostPos == newPosition and ghost._scaredTimer == 0):
                return float("-inf")

        # happy score if yellow man far from spooky poopy
        # score += 2 * minGhost
        # sad score if yellow man far from yummy tummy
        score -= 2 * minFood
        # big sad if yellow man isn't moving
        if action == 'STOP':
            score -= 100
        # happy if he eating
        if(successorGameState.getNumFood() < currentGameState.getNumFood()):
            score += 300

        return score

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    # Following pseudocode from this site
    # https://davideliu.com/2020/02/13/playing-pacman-with-multi-agents-adversarial-search/

    def minimax(self, depth, agent, gameState):
        # If the game has finished, return the value of the state
        if (gameState.isWin() or gameState.isLose() or depth > self.getTreeDepth()):
            evaluationFunction = self.getEvaluationFunction()
            return evaluationFunction(gameState)

        # Get possible actions for the agent without stops
        possibleActions = gameState.getLegalActions(agent)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)

        possibleScores = []
        # If it's the maximizer's turn (the player is the agent 0)
        if agent == 0:
            # Maximize the player's score and pass the next turn to the first ghost (agent 1)
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                possibleScores.append(self.minimax(depth, 1, successor))
            # If we're back to the root, we return an action based on max score
            if (depth == 1):
                for i in range(len(possibleScores)):
                    if (possibleScores[i] == max(possibleScores)):
                        return possibleActions[i]
            # Else return the max score
            else:
                return max(possibleScores)

        # If it's the minimizer's turn (the ghosts are the agent 1 to num_agents)
        else:
            # Get the index of the next agent
            nextAgent = agent + 1
            num_agents = gameState.getNumAgents()
            # If all agents have moved, then the next agent is the player
            if num_agents == nextAgent:
                nextAgent = 0
            # Increase depth every time all agents have moved
            if nextAgent == 0:
                depth += 1
            # Minimize ghost's score and pass the next ghost
            # OR the player if all ghosts have already moved
            # print("num_agents: " + str(num_agents) + " nextAgent: " +
            # str(nextAgent) + " depth: " + str(depth))
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                possibleScores.append(self.minimax(depth, nextAgent, successor))
            return min(possibleScores)

    def getAction(self, gameState):
        depth = 1
        agent = 0
        return self.minimax(depth, agent, gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def alphaBeta(self, depth, agent, gameState, oldAlpha, oldBeta):
        alpha = oldAlpha
        beta = oldBeta
        # If the game has finished, return the value of the state
        if (gameState.isWin() or gameState.isLose() or depth > self.getTreeDepth()):
            evaluationFunction = self.getEvaluationFunction()
            return evaluationFunction(gameState)

        # Get possible actions for the agent without stops
        possibleActions = gameState.getLegalActions(agent)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)

        possibleScores = []
        # If it's the maximizer's turn (the player is the agent 0)
        if agent == 0:
            # Maximize the player's score and pass the next turn to the first ghost (agent 1)
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                score = self.alphaBeta(depth, 1, successor, alpha, beta)

                # Prune unnecessary branches
                if (agent == 0 and score > beta):
                    return score
                if (agent > 0 and score < alpha):
                    return score
                # Set new alpha and beta
                if (agent == 0 and score > alpha):
                    alpha = score
                if (agent > 0 and score < beta):
                    beta = score

                possibleScores.append(score)

            # If we're back to the root, we return an action based on max score
            if (depth == 1):
                for i in range(len(possibleScores)):
                    if (possibleScores[i] == max(possibleScores)):
                        return possibleActions[i]
            # Else return the max score
            else:
                return max(possibleScores)

        # If it's the minimizer's turn (the ghosts are the agent 1 to num_agents)
        else:
            # Get the index of the next agent
            nextAgent = agent + 1
            num_agents = gameState.getNumAgents()
            # If all agents have moved, then the next agent is the player
            if num_agents == nextAgent:
                nextAgent = 0
            # Increase depth every time all agents have moved
            if nextAgent == 0:
                depth += 1
            # Minimize ghost's score and pass the next ghost
            # OR the player if all ghosts have already moved
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                score = self.alphaBeta(depth, nextAgent, successor, alpha, beta)

                # Prune unnecessary branches
                if (agent == 0 and score > beta):
                    return score
                if (agent > 0 and score < alpha):
                    return score
                if (agent == 0 and score > alpha):
                    alpha = score
                if (agent > 0 and score < beta):
                    beta = score

                possibleScores.append(score)
            return min(possibleScores)

    def getAction(self, gameState):
        depth = 1
        agent = 0
        alpha = float("-inf")
        beta = float("inf")
        return self.alphaBeta(depth, agent, gameState, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    # Following pseudocode from this site
    # https://davideliu.com/2020/02/13/playing-pacman-with-multi-agents-adversarial-search/

    def expectiMax(self, depth, agent, gameState):
        # If the game has finished, return the value of the state
        if (gameState.isWin() or gameState.isLose() or depth > self.getTreeDepth()):
            evaluationFunction = self.getEvaluationFunction()
            return evaluationFunction(gameState)

        # Get possible actions for the agent without stops
        possibleActions = gameState.getLegalActions(agent)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)

        possibleScores = []
        # If it's the maximizer's turn (the player is the agent 0)
        if agent == 0:
            # Maximize the player's score and pass the next turn to the first ghost (agent 1)
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                possibleScores.append(self.expectiMax(depth, 1, successor))
            # If we're back to the root, we return an action based on max score
            if (depth == 1):
                for i in range(len(possibleScores)):
                    if (possibleScores[i] == max(possibleScores)):
                        return possibleActions[i]
            # Else return the max score
            else:
                return max(possibleScores)

        # If it's the minimizer's turn (the ghosts are the agent 1 to num_agents)
        else:
            # Get the index of the next agent
            nextAgent = agent + 1
            num_agents = gameState.getNumAgents()
            # If all agents have moved, then the next agent is the player
            if num_agents == nextAgent:
                nextAgent = 0
            # Increase depth every time all agents have moved
            if nextAgent == 0:
                depth += 1
            # Expectimax for ghost's score and pass the next ghost
            # OR the player if all ghosts have already moved
            for action in possibleActions:
                successor = gameState.generateSuccessor(agent, action)
                possibleScores.append(self.expectiMax(depth, nextAgent, successor))
            return sum(possibleScores) / len(possibleScores)

    def getAction(self, gameState):
        depth = 1
        agent = 0
        return self.expectiMax(depth, agent, gameState)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    # def getAction(self, gameState):
    #     return 0
