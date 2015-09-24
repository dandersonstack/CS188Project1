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
import sys
import copy

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

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    initial_board_state=problem.getStartState()
    current_max_depth=1
    list_of_moves=[]
    while(list_of_moves == []):
        print(current_max_depth)
        list_of_moves=DepthLimitedSearch(problem,current_max_depth)
        current_max_depth+=1
    print('about to return!')
    return list_of_moves

def DepthLimitedSearch(problem, current_max_depth):
    from util import Stack
    from util import Counter
    from game import Actions
    from game import GameStateData
    start_board_state=problem.getStartState()
    current_board_state=start_board_state
    list_of_actions=Stack()
    seen_game_states=Counter()
    seen_game_states.update({current_board_state: current_board_state})
    while(True):
        current_possible_actions = problem.getActions(current_board_state)
        move_made=False
        if(problem.goalTest(current_board_state)):
            break
        if(current_max_depth <= len(list_of_actions.list)):
            most_recent_move=list_of_actions.pop()
            current_board_state= problem.getResult(current_board_state,Actions.reverseDirection(most_recent_move))
            continue
        else:
            current_possible_actions = problem.getActions(current_board_state)
            possible_new_board_state = current_board_state
            if(current_possible_actions and not move_made):
                for i in range(len(current_possible_actions)):
                    possible_new_board_state = problem.getResult(current_board_state,current_possible_actions[i])
                    print(current_possible_actions)
                    if(possible_new_board_state not in seen_game_states.values()):
                        #make the move and update the problem
                        list_of_actions.push(current_possible_actions[i])
                        seen_game_states.update({possible_new_board_state: possible_new_board_state})
                        current_board_state=possible_new_board_state
                        current_possible_actions = problem.getActions(current_board_state)
                        #seen_game_states[seen_game_states.argMax()+1] = current_board_state
                        continue
            if(not move_made):
                if(list_of_actions.isEmpty()):
                    break
                most_recent_move=list_of_actions.pop()
                current_board_state= problem.getResult(current_board_state,Actions.reverseDirection(most_recent_move))
    return list_of_actions.list


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import PriorityQueueWithFunction
    from util import Stack
    from util import Counter
    closed = set()
    fringe = util.PriorityQueue()   #A* uses priorityqueue
    fringe.push( [problem.getStartState(), list()], 0)    #fringe node is [pos(x,y),move_list,cost]
    while not fringe.isEmpty():
        node = fringe.pop()
        
        if problem.goalTest(node[0]): #passes coordinates
            return node[1]  #list of directions

        if node[0] not in closed:
            closed.add(node[0])
            for child in problem.getSuccessors(node[0]):
                actions = node[1]+[child[1]]
                fringe.push( [child[0] , actions], problem.getCostOfActions(actions)+heuristic(child[0],problem) )


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
