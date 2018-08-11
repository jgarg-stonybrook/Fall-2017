# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    flag = 0

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print(chosenIndex)
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #calculate if the current position is a ghost position or not. If it is then return a low (-2) score.
        #also calculate the average ghost distance from current position.
        ghostDistance=0
        gd=[]
        for ghostState in newGhostStates:
            ghostPos=ghostState.getPosition()
            tmpDist = (abs(newPos[0]-ghostPos[0])+abs(newPos[1]-ghostPos[1]))
            if tmpDist == 0:
                return -2
            ghostDistance += tmpDist
            gd.append(ghostDistance)

        ghostDistance /= len(newGhostStates)


        foods= list(newFood)
        x= len(foods)
        y= len(foods[0])

        minFoodDist = 100000
        foodCount=0
        oldFoodCount=0
        oldFood=currentGameState.getFood()

        #calculate the minimum food distance from PacMan, the difference of the total food count from previous position
        #and the current position (it will either be a 0 or a 1)
        for i in range(0,x):
            for j in range(0,y):
                if newFood[i][j]:
                    foodCount += 1
                    foodDist = abs(newPos[0]-i)+abs(newPos[1]-j)
                    if foodDist < minFoodDist and foodDist != 0:
                        minFoodDist = foodDist

                if currentGameState.hasFood(i,j):
                    oldFoodCount += 1

        #this is the last food: eat it
        if minFoodDist == 100000:
            minFoodDist = 0

        foodCount=abs(foodCount-oldFoodCount)

        #Normalize the values of Foodcoun
        rowXCol=(x-2)*(y-2)
        normFoodCount = float(foodCount)
        normGhostDist= float(ghostDistance)/((x-2-1)+(y-2-1))
        normFoodDist = float(minFoodDist)/((x-2-1)+(y-2-1))

        #ghost distance is too far so it won't contribute the the evaluation function.
        if ghostDistance >= 5:
            normGhostDist = 0

        #some ghost is too close: so make PacMan run away from there
        for dist in gd:
            if dist <= 1:
                normGhostDist = -2

        #calculate the evaluation function using total foodCount, minimum food distance and average ghost distance as parameters
        #also to make PacMan not remain stationary at current position deduct a factor of 0.4
        if newPos == currentGameState.getPacmanPosition():
            return float(float(normFoodCount) + (1-float(normFoodDist)) + (float(normGhostDist))) - 0.4
        else:
            return float(
                float(normFoodCount) + (1-float(normFoodDist)) + (float(normGhostDist)))

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.turn = 1

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # Pathfinder is a function that will return the best action for the pacman according to the given algorithm
        # arguments (gamestate, currentdepth of Search Tree,Whose Turn Pacman or Ghost, Agent Number
        self.maxdepth = self.depth * gameState.getNumAgents()
        return self.pathFinder(gameState,0,0,0)

    def pathFinder(self,gameState,currentDepth,minmax,agent):
        maxList = []
        minList = []
        if currentDepth == self.maxdepth:
            return self.evaluationFunction(gameState)

        if minmax  == 0:
            # Turn for Pacman
            actionList = []
            legalActionList = gameState.getLegalActions(agent)
            # if legal action list is empty that means it is terminal state so return the value of selfEvaluationFunction
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            for agentAction in legalActionList:
                # Generate successors for Pacman
                successorGameState = gameState.generateSuccessor(agent, agentAction)
                # Call for Ghost by changing minmax = 1, agent+1 and increase depth of minmax tree by 1
                num = self.pathFinder(successorGameState,currentDepth+1,1,agent+1)
                # Append the result to maxList and store the corresponding action in actionList
                maxList.append(num)
                actionList.append(agentAction)
            # Choose the max value at max node and pass the max value to above minnode or return action if depth is 0
            maxi = max(maxList)
            index = maxList.index(maxi)
            actionToreturn = actionList.pop(index)
            if currentDepth == 0:
                return actionToreturn
            else:
                return maxi
        elif minmax == 1:
            # Turn for Ghost
            ghostAgents = gameState.getNumAgents()-1
            legalActionList = gameState.getLegalActions(agent)
            num = 0
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            else:
                for agentAction in legalActionList:
                    successorGameState = gameState.generateSuccessor(agent, agentAction)
                    # if this is last ghost , give the turn to pacman by putting minmax = 0 else if next is also ghost then
                    # put minmax = 0 for next call
                    if agent == ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 0, 0)
                    elif agent < ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 1, agent+1)
                    minList.append(num)
                # Here the ghost will only return the minimum of all returned values.
                mini = min(minList)
                return mini


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # The maxdepth of tree could only be ply * number of agents in the game
        self.maxdepth = self.depth * gameState.getNumAgents()
        # Pathfinder is a function that will return the best action for the pacman according to the given algorithm
        # arguments (gamestate, currentdepth of Search Tree,Whose Turn Pacman or Ghost, Agent Number,beta = inf,alpha = -inf
        return self.pathFinder(gameState, 0, 0, 0,99999,-99999)


    def pathFinder(self,gameState,currentDepth,minmax,agent,beta,alpha):
        maxList = []
        minList = []
        if currentDepth == self.maxdepth:
            return self.evaluationFunction(gameState)

        if minmax  == 0:
            # Turn for Pacman
            actionList = []
            # if legal action list is empty that means it is terminal state so return the value of selfEvaluationFunction
            legalActionList = gameState.getLegalActions(agent)
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            for agentAction in legalActionList:
                # Generate successors for Pacman
                successorGameState = gameState.generateSuccessor(agent, agentAction)
                # Call for Ghost by changing minmax = 1, agent+1 and increase depth of minmax tree by 1
                num = self.pathFinder(successorGameState,currentDepth+1,1,agent+1,beta,alpha)
                # if the value returned by child node is greater than alpha, so we update alpha at maxnode as alpha always
                # increases and we dont need to call for other actions as the pacman is never going to choose them
                if num > alpha:
                    alpha = num
                if num > beta:
                    return num
                maxList.append(num)
                actionList.append(agentAction)
            # Choose the max value at max node and pass the max value to above minnode or return action if depth is 0
            maxi = max(maxList)
            index = maxList.index(maxi)
            actionToreturn = actionList.pop(index)
            if currentDepth == 0:
                return actionToreturn
            else:
                return maxi
        elif minmax == 1:
            # Turn for Ghost
            ghostAgents = gameState.getNumAgents()-1
            legalActionList = gameState.getLegalActions(agent)
            num = 0
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            else:
                for agentAction in legalActionList:
                    successorGameState = gameState.generateSuccessor(agent, agentAction)
                    # if this is last ghost , give the turn to pacman by putting minmax = 0 else if next is also ghost then
                    # put minmax = 0 for next call
                    if agent == ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 0, 0,beta,alpha)
                    elif agent < ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 1, agent+1,beta,alpha)
                    # if the value returned by child node is lesser than beta, so we update beta at minnode as beta always
                    # decreses and we dont need to call for other actions as the ghost is never going to choose them
                    if num < beta:
                        beta = num
                    if num < alpha:
                        return num
                    minList.append(num)
                mini = min(minList)
                return mini

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # The maxdepth of tree could only be ply * number of agents in the game
        self.maxdepth = self.depth * gameState.getNumAgents()
        # Pathfinder is a function that will return the best action for the pacman according to the given algorithm
        # arguments (gamestate, currentdepth of Search Tree,Whose Turn Pacman or Ghost, Agent Number
        return self.pathFinder(gameState, 0, 0, 0)


    def pathFinder(self,gameState,currentDepth,minmax,agent):
        maxList = []
        minList = []
        if currentDepth == self.maxdepth:
            return self.evaluationFunction(gameState)

        if minmax  == 0:
            # Turn for Pacman
            actionList = []
            # if legal action list is empty that means it is terminal state so return the value of selfEvaluationFunction
            legalActionList = gameState.getLegalActions(agent)
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            for agentAction in legalActionList:
                # Generate successors for Pacman
                successorGameState = gameState.generateSuccessor(agent, agentAction)
                # Call for Ghost by changing minmax = 1, agent+1 and increase depth of minmax tree by 1
                num = self.pathFinder(successorGameState,currentDepth+1,1,agent+1)
                # Append the result to maxList and store the corresponding action in actionList
                maxList.append(num)
                actionList.append(agentAction)
            # Choose the max value at max node and pass the max value to above minnode or return action if depth is 0
            maxi = max(maxList)
            index = maxList.index(maxi)
            actionToreturn = actionList.pop(index)
            if currentDepth == 0:
                return actionToreturn
            else:
                return maxi
        elif minmax == 1:
            # Turn for Ghost
            ghostAgents = gameState.getNumAgents()-1
            legalActionList = gameState.getLegalActions(agent)
            num = 0
            if len(legalActionList) == 0:
                return self.evaluationFunction(gameState)
            else:
                for agentAction in legalActionList:
                    successorGameState = gameState.generateSuccessor(agent, agentAction)
                    # if this is last ghost , give the turn to pacman by putting minmax = 0 else if next is also ghost then
                    # put minmax = 0 for next call
                    if agent == ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 0, 0)
                    elif agent < ghostAgents:
                        num = self.pathFinder(successorGameState, currentDepth + 1, 1, agent+1)
                    minList.append(num)
                # Here the ghost will only return the average of all returned values.
                mini = sum(minList)/float(len(legalActionList))
                return mini

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

