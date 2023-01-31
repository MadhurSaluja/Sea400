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

def depthFirstSearch(problem: SearchProblem):
    """
       Search the deepest nodes in the search tree first.
       Your search algorithm needs to return a list of actions that reaches the
       goal. Make sure to implement a graph search algorithm.
       To get started, you might want to try some of these simple commands to
       understand the search problem that is being passed in:
       print("Start:", problem.getStartState())
       print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
       print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    """
    Pseudo code from https://inst.eecs.berkeley.edu/~cs188/sp20/assets/notes/n1.pdf
    to tell us the generic solution.
    Function Algorithms(problem, fringe) return a solution #I believe that would be a list# or failure
        fringe <- Insert(push node in the stack)
        loop do
            if fringe is empty then return faliure
            node <- Remove-Front(fringe)
            visited<-node

            if Goal-Test(problem, STATE[node]) then return node 
            for child node in Expand(STATE[node], problem) do
            fringe<-INSERT(child,fringe)
            end
        end
    """
#Util.Stack should be used as the data structure 
    # as it has a the same concept of LIFO, also there should be 
    # a stack for expanded node; and a backtrack to successfull expansion
    Fringe=util.Stack()
    expanded=[] #To keep track of all expanded nodes
    child_nodes=[]
    #give the frontier(fringe) it's first node;
    #Node: define a data structure with state,name, parent, action. For simplicity I 
    #chose to only have state and path to the goal as a tuple as that is only required for that.

    # inspired by https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    Node=((problem.getStartState(),child_nodes)) # The tuple consist of state and list of expanded paths
    #push the Node 
    Fringe.push(Node)
    #check if there are any nodes in the fringe 
    while  not Fringe.isEmpty():
        frontier=Fringe.pop()
        # if there is a node then move it out of the stack to work on it
        # append the state of a frontier to the expanded list
        #so that state shouldn't be repeated.

        expanded.append(frontier[0])
         # check if the frontier is the goal
        if problem.isGoalState(frontier[0]):
            return frontier[1]
        else:
             #Get the successors from the current state
             successors = problem.getSuccessors(frontier[0])
             #make sure the successors aren't already expanded
             for successor in successors:
                 if not successor[0] in expanded:
                    Fringe.push((successor[0],frontier[1]+ [successor[1]]))
   
    return []
 




# REFERENCE :: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #keeping the pseudocode from the dfs search (excpet use Queue)
    Fringe=util.Queue()
    child_nodes=[]
    Node=((problem.getStartState(),child_nodes))
    Fringe.push(Node)
    Expanded=[]

    while not Fringe.isEmpty():
        frontier= Fringe.pop()
        Expanded.append(frontier[0])
        if problem.isGoalState(frontier[0]):
            return frontier[1]
        else:
            successors=problem.getSuccessors(frontier[0])
            for successor in successors:
                if not successor[0]  in Expanded:
                 Fringe.push((successor[0],frontier[1]+ [successor[1]]))
                 Expanded.append(successor[0])

    return []

            
  #  util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    reached = {}      # has the nodes which are popped from queue
    result = []       # has the listed directions for pacman to reach to goal state
    queue = util.PriorityQueue()  # has nodes in the fringe list, cost and direction
    parents = {}   # has nodes and their parents
    cost = {}      # has nodes and their costs

    start = problem.getStartState()
    queue.push((start, 'Undefined', 0), 0)
    reached[start] = 'Undefined'
    cost[start] = 0    #cost of start state is zero

    if problem.isGoalState(start):
        return result
    
    goal = False;
    while(goal != True and queue.isEmpty()  != True):
        # loop while queue is not null and goal is not yet reached
        node = queue.pop()
        reached[node[0]] = node[1]
        if problem.isGoalState(node[0]):
            node_result = node[0]
            goal = True
            break
        # further expanding node
        for key in problem.getSuccessors(node[0]):
            if key[0] not in reached.keys():
                priority = node[2] + key[2]
                if key[0] in cost.keys():
                    if cost[key[0]] <= priority:
                        continue
                queue.push((key[0], key[1], priority), priority)
                cost[key[0]] = priority
                parents[key[0]] = node[0]
    # storing and searching for path
    while(node_result in parents.keys()):
        node_result_initial = parents[node_result]
        result.insert(0, reached[node_result])
        node_result = node_result_initial

    return result

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Fringe=util.PriorityQueue()
    child_nodes=[]
    start_cost = 0
    Node=(problem.getStartState(),child_nodes, start_cost)
    Fringe.push(Node, start_cost)
    Expanded=[]

    while not Fringe.isEmpty():
        frontier= Fringe.pop()
        if frontier[0] not in Expanded:
            Expanded.append(frontier[0])
            if problem.isGoalState(frontier[0]):
                return frontier[1]
            else:
                successors=problem.getSuccessors(frontier[0])
                for successor in successors:
                    if not successor[0]  in Expanded:
                        next_successor = frontier[1] + [successor[1]]
                        cost = frontier[2] + successor[2]
                        heuristiccost = cost + heuristic(successor[0], problem)
                        Fringe.push((successor[0],next_successor, cost), heuristiccost)
                        # Expanded.append(successor[0])

    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
