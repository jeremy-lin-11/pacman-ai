"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    I made the noise really small so that the agent is less likely
    to end up in an unintended successor state when they perform an
    action.
    """

    answerDiscount = 0.9
    answerNoise = 0.0001

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    Decreased discount so higher penalty for taking more moves.
    Decreased noise so likely to take risk
    """

    answerDiscount = 0.3
    answerNoise = 0.0001
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    decrease discount for same as last
    higher noise so more risk averse
    """

    answerDiscount = 0.3
    answerNoise = 0.1
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    discount high so less penalty for more moves
    low noise so less risk averse
    """

    answerDiscount = 0.9
    answerNoise = 0.0001
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    change nothing, already incentivize more moves
    and less risk
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    no penalty on moves
    always go exactly where it chooses
    no penalty for staying alive
    makes it avoid everything and get stuck

    """

    answerDiscount = 1.0
    answerNoise = 0.0
    answerLivingReward = 1.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    """

    answerEpsilon = 0.3
    answerLearningRate = 0.5

    return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
