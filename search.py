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
    from util import Stack
    from util import Counter
    from game import Actions
    from game import GameStateData
    from searchAgents import PositionSearchProblem
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    initial_board_state=problem.getStartState()
    current_max_depth,current_depth=1,0

    while(True):
        current_board_state=problem.getStartState()
        list_of_actions=Stack()
        seen_game_states=Counter()
        seen_game_states.update({hash(current_board_state): current_board_state})
        while(current_max_depth >= current_depth):
            move_made_this_iteration=False
            current_possible_actions = PositionSearchProblem.getActions(problem,current_board_state)

            if(current_possible_actions):
                for i in range(len(current_possible_actions)):
                    if(not move_made_this_iteration):
                        possible_new_board_state = PositionSearchProblem.getResult(problem,current_board_state,current_possible_actions[i])
                        if(possible_new_board_state not in seen_game_states.values()):
                            #make the move and update the problem
                            list_of_actions.push(current_possible_actions[i])
                            current_board_state=possible_new_board_state
                            seen_game_states.update({hash(current_board_state): current_board_state})
                            #seen_game_states[seen_game_states.argMax()+1] = current_board_state
                            move_made_this_iteration=True
                            current_depth+=1
                            if(PositionSearchProblem.goalTest(problem, current_board_state)):
                                return list_of_actions.list
            if(not move_made_this_iteration):
                if(list_of_actions.isEmpty()):
                    print 'something went wrong'
                    return 'no solution'
                most_recent_move=list_of_actions.pop()
                current_board_state= PositionSearchProblem.getResult(problem,current_board_state,Actions.reverseDirection(most_recent_move))
                if(current_depth == 0):
                    print 'something went wrong'
                    return 'no solution'
                current_depth-=1
        current_max_depth+=1
        current_depth=0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import PriorityQueueWithFunction
    from util import Stack
    from util import Counter

    import copy
    from searchAgents import PositionSearchProblem


    #initialization
    game_states_visited_plus_path_to_them=Counter()
    current_board_state=problem.getStartState()
    current_list_of_moves=[]
    game_states_visited_plus_path_to_them[hash(current_board_state)] = (current_board_state,current_list_of_moves)

    #the priority queue is a list of games state action pairs
    #by gamestates I mean the old game state that has already been expanded.
    possible_states_to_expand=PriorityQueue()

    #a list of possible actions that can be taken from the current board
    current_possible_actions = PositionSearchProblem.getActions(problem,current_board_state)
    print('here is what the board state looks like')
    print(current_board_state)
    #we now initialize the priorityque with a list of boardstate,action pairs
    #the priority is set internally but we could write a lamda function for it.
    for i in range(len(current_possible_actions)):
        possible_new_board_state = PositionSearchProblem.getResult(problem,current_board_state,current_possible_actions[i])
        priority=heuristic(possible_new_board_state,problem) + 1
        possible_states_to_expand.push((current_board_state,current_possible_actions[i]), priority * -1)

    print('initial set of possible move pairs')
    print('the priorityqueu itself')
    print(possible_states_to_expand.heap)


    #we now expand each move, check if it is the goal state, if it is the goal state
    #we finish, else we find all surrounding moves and add them to the list of possible nodes
    while(not possible_states_to_expand.isEmpty()):

        #(current board state + a direction)
        #pop the best possible move from the stack
        board_action_tuple=possible_states_to_expand.pop()

        #we set the current board and the action we are about to take
        current_board_state = board_action_tuple[0]
        current_direction = board_action_tuple[1]

        #complete the move to get the new board state to explore
        new_board_state = PositionSearchProblem.getResult(problem,current_board_state,current_direction)

        #we must get the list of moves used to get to the current board state first
        current_list_of_moves = game_states_visited_plus_path_to_them.get(hash(current_board_state))[1]
        print(current_list_of_moves)
        #now we clone that stack and add the new move to it
        new_list_of_moves = copy.copy(current_list_of_moves)
        new_list_of_moves.append(current_direction)

        #check if the new_board_state wins the game
        if(PositionSearchProblem.goalTest(problem, new_board_state)):
            return new_list_of_moves

        #check if that gamestate already exists,
        #if it does not exist then merely update the dictionary
        if(hash(new_board_state) not in game_states_visited_plus_path_to_them):
            #now we create a new tuple with the new_board_state_and the list of moves we used to get ther
            #and we add that tuple to the list of visited game boards
            game_states_visited_plus_path_to_them.update({hash(new_board_state) : (new_board_state,new_list_of_moves)})
        else:
            old_number_of_moves_board_state = len(game_states_visited_plus_path_to_them.get(hash(current_board_state))[1])
            if(old_number_of_moves_board_state < len(current_list_of_moves)):
                game_states_visited_plus_path_to_them.update({hash(current_board_state) : (new_board_state,new_list_of_moves)})


        #now we need to search out all the possible new moves and add it to the priorityque
        #first pull up a list of actions we can make from the new board state
        current_possible_actions = PositionSearchProblem.getActions(problem,new_board_state)
        #check each move and add it to the priorityqueue
        for i in range(len(current_possible_actions)):
            possible_new_board_state = PositionSearchProblem.getResult(problem,new_board_state,current_possible_actions[i])
            if(hash(possible_new_board_state) != hash(current_board_state)):
                priority=heuristic(possible_new_board_state,problem) + len(new_list_of_moves)+1
                possible_states_to_expand.push((new_board_state,current_possible_actions[i]), priority * -1)
        # possible_new_board_state = PositionSearchProblem.getResult(problem,current_board_state,current_possible_actions[i])
        # game_states_visited.update({len(seen_game_states)+1 : current_board_state})
        # current_list_of_moves.push(current_possible_actions[i])


    """
    -first add the initial board state to the list of seen board states (a dictionary)
    -add a stack to an overlapping dictionary of moves used to get to that board state
    while(true)
        create a list of possible moves and calculate the values for each of those new board states
            -create priority que of every move by looking at all every board states
            -the number will be how many moves from the start, plus the necessary heuristic
        choose the first best possible move of that list of moves and check if you can expand it out.
            to check if you can expand it out
                -add the new board state to the list of seen board states
                    -if that board state does not exists
                        -take the stack of moves used to get to that point, from the previous board state
                        -add the new move, and then add the stack of moves + the board state to the dictionary
                        -then break out of the while loop and take the next node from the prioritQueue
                        -also take that new board state we just found and
                            -find the moves around it, and add those new possible moves to the priorityqueue
                    -else if that board state already exists then compare heights
                        -compare the associated stacks with the old list of moves and new list of moves
                            used to get to that board state
                        if the new list of moves is shorter
                            -then update that stack with the new stack
                        else if the old list of moves is shorter
                            -you do nothing
            else if you can't expand it out
                -don't worry about it, you still popped that move, now try the next possible move
    """

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
