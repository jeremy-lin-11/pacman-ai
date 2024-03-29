from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection, probability
# from pacai.core.featureExtractors import FeatureExtractor
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    DESCRIPTION: <Write something here so we know what you did.>
    Q-value agent has added exploration , allows it to train with adjustable
    learning rate and epsilon factor
    - benefitial when we cannot calculate the entire model beforehand like
    in many real world situations.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.qValues = {}

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        if (state, action) in self.qValues:
            return self.qValues[(state, action)]
        else:
            return 0.0

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        qValues = [self.getQValue(state, action) for action in self.getLegalActions(state)]
        if len(qValues) == 0:
            return 0.0
        else:
            return max(qValues)

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        value = self.getValue(state)
        actions = [action for action in
                   self.getLegalActions(state) if self.getQValue(state, action) == value]

        if len(actions) == 0:
            return None
        else:
            return random.choice(actions)

    def getAction(self, state):
        """
        Compute the action to take in the current state.
        With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
        we should take a random action and take the best policy action otherwise.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should choose None as the action.
        """
        actions = self.getLegalActions(state)

        if len(actions) == 0:
            return None
        elif probability.flipCoin(self.getEpsilon()):
            return random.choice(actions)
        else:
            return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a state transition and reward.
        You should do your Q-Value update here.
        Note that you should never call this function, it will be called on your behalf.
        """
        alpha = self.getAlpha()
        discountRate = self.getDiscountRate()
        qValue = self.getQValue(state, action)
        nextValue = self.getValue(nextState)

        updateValue = (1 - alpha) * qValue + alpha * (reward + discountRate * nextValue)
        self.qValues[(state, action)] = updateValue

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    Followed the equations for q9
    q value is now calculated by f(s,a) * w
    weights are updated with their corresponding features and learning rate
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def getWeight(self, key):
        return self.weights.get(key, 0.0)

    def getQValue(self, state, action):
        # features = FeatureExtractor.getFeatures(state, action)
        # print(state)
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        # print("features: \n", features)
        qValue = 0
        for feature in features:
            # print("feature: \n", feature)
            # state = feature[0]
            # print(state)
            qValue += self.getWeight(feature) * features[feature]
        return qValue

    def update(self, state, action, nextState, reward):
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        delta = (reward + self.discountRate * self.getValue(nextState)
                 ) - self.getQValue(state, action)
        for feature in features:
            self.weights[feature] = self.getWeight(feature) + (
                self.getAlpha() * delta * features[feature])

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            # print("weights: \n", self.weights.values())
            print("Weight Vector Length: ", len(self.weights))
            # raise NotImplementedError()
