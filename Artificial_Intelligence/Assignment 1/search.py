# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """
    Stack Data Structure is used to implement DFS.
    """

    # visitedList stores the nodes that have been visited while traversing the grid via DFS.
    # s is the stack which stores tuple of the form (state, actionList, cost)
    # state is the current Pac-Man position.
    # actionList is the list of actions required to get from the initial Pac-Man position to the 'state' position.
    # cost is the cost/distance up to the current position.

    s = util.Stack()
    visitedList = {}

    s.push((problem.getStartState(), [], 0))

    while not s.isEmpty():

        (state, actionlist, cost) = s.pop()

        #If GoalState has been reached then return the actionList
        if problem.isGoalState(state):
            return actionlist

        #Push all successors of the current state that have not yet been visited onto the stack with the appropriate
        # (state, actionList, cost) tuple.
        if state not in visitedList:
            visitedList[state] = True
            for successor, act, c in problem.getSuccessors(state):
                if successor:
                    if successor not in visitedList:
                        s.push((successor, actionlist + [act], c + cost))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """
    BFS is implemented using the Queue Data Structure.
    """

    # visitedList stores the nodes that have been visited while traversing the grid via BFS.
    # q is the queue which stores tuple of the form (state, actionList, cost)
    # state is the current Pac-Man position.
    # actionList is the list of actions required to get from the initial Pac-Man position to the 'state' position.
    # cost is the cost/distance up to the current(state) position.

    q = util.Queue()
    visitedList = {}

    q.push((problem.getStartState(), [], 0))

    while not q.isEmpty():

        (state, actionlist, cost) = q.pop()

        # If GoalState has been reached then return the actionList
        if problem.isGoalState(state):
            return actionlist

        # Push all successors of the current state that have not yet been visited onto the queue with the appropriate
        # (state, actionList, cost) tuple.
        if state not in visitedList:
            visitedList[state] = True
            for successor, act, c in problem.getSuccessors(state):
                if successor:
                    if successor not in visitedList:
                        q.push((successor, actionlist + [act], c + cost))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
        UCS is implemented using the Priority Queue Data Structure.
    """
    # visitedList stores the nodes that have been visited while traversing the grid via UCS.
    # pq is the priority queue which stores tuple of the form ((state, actionList, cost), priority)
    # state is the current Pac-Man position.
    # actionList is the list of actions required to get from the initial Pac-Man position to the 'state' position.
    # cost is the cost/distance up to the current(state) position.
    # priority queue also takes in the priority value which is the cost value for this case.

    pq=util.PriorityQueue()
    visitedList={}

    pq.push((problem.getStartState(), [], 0), 0)

    while not pq.isEmpty():

        (state, actionlist, cost)=pq.pop()

        # If GoalState has been reached then return the actionList
        if problem.isGoalState(state):
            return actionlist

        # Push all successors of the current state that have not yet been visited onto the priority queue with
        #  the appropriate ((state, actionList, cost), priority) tuple.
        if state not in visitedList:
            visitedList[state] = True
            for successor, act, c in problem.getSuccessors(state):
                if successor:
                    if successor not in visitedList:
                        pq.push((successor, actionlist+[act], c+cost), c+cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    aStarSearch is implemented using the Priority Queue Data Structure along with a heuristic function.
    """

    # visitedList stores the nodes that have been visited while traversing the grid via aStarSearch.
    # pq is the priority queue which stores tuple of the form (state, actionList, cost)
    # state is the current Pac-Man position.
    # actionList is the list of actions required to get from the initial Pac-Man position to the 'state' position.
    # cost is the cost/distance up to the current(state) position.

    #priority queue takes in the heuristic value + cost value as its priority value.

    pq = util.PriorityQueue()
    visitedList = {}

    pq.push((problem.getStartState(), [], 0), 0)

    while not pq.isEmpty():

        (state,actionlist,cost) = pq.pop()

        # If GoalState has been reached then return the actionList
        if problem.isGoalState(state):
            return actionlist

        # Push all successors of the current state that have not yet been visited onto the priority queue with
        #  the appropriate ((state, actionList, cost), priority) tuple.
        if state not in visitedList:
            visitedList[state] = True
            for successor, act, c in problem.getSuccessors(state):
                if successor:
                    if successor not in visitedList:
                        pq.push((successor, actionlist+[act], cost+c),
                                cost+c+heuristic(successor, problem))

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
