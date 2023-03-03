from pacai.agents.learning.value import ValueEstimationAgent
# from pacai.core.mdp import MarkovDecisionProcess
# import random

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        # For each state, calculate the Q* of the state with all of its possible actions
        for i in range(iters):
            newValues = self.values.copy()
            # print(self.mdp.getStates())
            for state in self.mdp.getStates():
                optimalAction = self.getAction(state)
                if optimalAction is not None:
                    newValues[state] = self.getQValue(state, optimalAction)

            self.values = newValues

        # raise NotImplementedError()

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        value = self.values.get(state, 0.0)
        # print("getValue --- \nreturn: ", value, "\n")
        return value

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """
        action = self.getPolicy(state)
        # print("getAction --- \nreturn: ", action, "\n")
        return action

    def getQValue(self, state, action):
        # Q*(s,a) = sum of (transitions * (reward + discount*value))
        # print("--- getQvalue --- \nstate: ", state, " action: ", action, "\n")
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0
        for nextState, prob in transitions:
            # print(self.values)
            reward = self.mdp.getReward(state, action, nextState)
            qValue += prob * (reward + self.discountRate * self.getValue(nextState))

        return qValue

    def getPolicy(self, state):
        # print("--- getPolicy --- \nstate: ", state, "\n")
        if self.mdp.isTerminal(state):
            # print("--- getPolicy --- return: None\n")
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            optimalQ = self.getQValue(state, actions[0])
            optimalPolicy = actions[0]

            for action in actions:
                qValue = self.getQValue(state, action)
                if optimalQ < qValue:
                    optimalQ = qValue
                    optimalPolicy = action
            # print("--- getPolicy --- return: ", optimalPolicy, "\n")
            return optimalPolicy
