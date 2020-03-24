import math
import sys

'''
Class Node
'''
class Node:
    def __init__(self,x,y,priority,came_from=None, cost_so_far = 0):
        self.x = x
        self.y = y
        self.priority = priority
        self.came_from = came_from
        self.cost_so_far = cost_so_far

    '''
    Function neighbors returns all the neighbor nodes
    when type == a, the algorithm assumes that the agent can move up, down, left, and right,
    but not diagonally.In best scenerio, the node has four neighbors.
    when type == b, the algorithm assumes that the agent can move up, down, left, and right,
    and diagonally. In best scenerio, the node has eight neighbors.
    '''
    def neighbors(self,type,maze):
        all_possible_neighbors = []
        neighbors = []
        x = self.x
        y = self.y
        if type == 'a':
            all_possible_neighbors += [[x-1,y], [x+1,y], [x,y-1],[x,y+1]]
        else:
            all_possible_neighbors += [[x-1,y], [x+1,y], [x,y-1],[x,y+1],[x-1,y-1],[x-1,y+1],[x+1,y-1],[x+1,y+1]]

        for node in all_possible_neighbors:
            nodex = node[0] - 1
            nodey = node[1] - 1
            #if the node is in maze boundaries
            if nodex > 0 and nodey > 0:
                node_value = maze[nodey][nodex]
                if node_value == '_' or node_value == 'G' or node_value == 'S':
                    neighbors.append([nodex+1, nodey+1])
        return neighbors

    '''
    Function is_node compares if two nodes are the same. If two nodes are the same, the function
    returns True; if two nodes are different, the function returns False
    '''
    def is_node(self,node):
        return self.x == node[0] and self.y == node[1]

    
    #Function cost returns the Euclidean distance between two nodes
    def cost(self, node):
        return math.sqrt(math.pow(abs(self.x-node[0]),2) + math.pow(abs(self.y-node[1]),2))


'''
Function greedySearch finds a path between the start position and the goal
position using Greedy algorithm.
When type == a, it assumes that the agent can move up, down, left, and right,
but not diagonally. The cost of moving up, down, left, or right is 1.
When type == b, it assumes that the agent can move up, down, left, and right,
and diagonally. The cost of moving up, down, left, right or diagonal is 1.
'''
def greedySearch(maze ,start, goal,type):
    startNode = Node(start[0], start[1],0)
    frontier = [startNode]
    visited = [start]
    visitedNode = []

    while len(frontier)!=0:
        #the code simulates priority queue and pops out the node with the lowest priority
        min = sys.maxsize
        for node in frontier:
            if node.priority < min:
                currentNode = node
                min = node.priority
        frontier.remove(currentNode)
        visitedNode.append(currentNode)
        visited.append([currentNode.x, currentNode.y])

        #searching stops when goal is reached
        if currentNode.is_node(goal):
            break
        for next in currentNode.neighbors(type,maze):
            if next not in visited:
                priority = heuristic(goal, next)
                newNode = Node(next[0], next[1], priority, currentNode)
                frontier.append(newNode)

    path = find_path(visitedNode, start, goal)
    #strips down the start node and the goal node
    if len(path) > 2:
        path.remove(path[0])
        path.pop()

    if type == 'a':
        write_output_to_file("pathfinding_a_out.txt", "Greedy", path,maze)
    else:
        write_output_to_file("pathfinding_b_out.txt", "Greedy", path,maze)


'''
Function aStarSearch finds a path between the start position and the goal
position using A* algorithm.
When type == a, it assumes that the agent can move up, down, left, and right,
but not diagonally. The cost of moving up, down, left, or right is 1.
When type == b, it assumes that the agent can move up, down, left, and right,
and diagonally. The cost of moving up, down, left, right or diagonal is 1.
'''
def aStarSearch(maze ,start, goal,type):
    startNode = Node(start[0], start[1],0)
    frontier = [startNode]
    visited = [start]
    visitedNode = []

    while len(frontier)!=0:
        #the code simulates priority queue and pops out the node with the lowest priority
        min = sys.maxsize
        for node in frontier:
            if node.priority < min:
                currentNode = node
                min = node.priority
        frontier.remove(currentNode)
        visitedNode.append(currentNode)
        visited.append([currentNode.x, currentNode.y])
        
        #searching stops when goal is reached
        if currentNode.is_node(goal):
            break

        #loop through all the neighbors 
        for next in currentNode.neighbors(type,maze):
            new_cost = currentNode.cost_so_far + currentNode.cost(next)
            priority = heuristic(goal, next) + new_cost
            # If the node has been visited but has lesser cost, the path will be replanned
            if next in visited:
                nextNode = findNode(visitedNode, next) 
                if new_cost < nextNode.cost_so_far:
                    newNode = Node(next[0], next[1], priority, currentNode, new_cost)
                    frontier.append(newNode)
            # If the node hasn't been visited
            else:
                newNode = Node(next[0], next[1], priority, currentNode, new_cost)
                frontier.append(newNode)         

    path = find_path(visitedNode, start, goal)
    #strips down the start node and the goal node
    if len(path) > 2:
        path.remove(path[0])
        path.pop()

    if type == 'a':
        write_output_to_file("pathfinding_a_out.txt", "A*", path,maze)
    else:
        write_output_to_file("pathfinding_b_out.txt", "A*", path,maze)


'''
helper function to find the corresponding node for pair(x,y)
'''
def findNode(node_list, target):
    for node in node_list:
        if node.x == target[0] and node.y == target[1]:
            return node

'''
Heuristic function returns the Euclidean distance between the goal and the given
node
'''
def heuristic(goal, next):
    return math.sqrt(math.pow(abs(goal[0] - next[0]),2) + math.pow(abs(goal[1]-next[1]),2))


'''
Function find_path returns a list containing all the nodes in the searching path if
the goal is found, returns None otherwise
'''
def find_path(visited_node,start, goal):
    path = []
    currentNode = visited_node.pop()
    if currentNode.is_node(goal) == False:
        return None
    else:
        while currentNode.is_node(start) == False:
            path.append(currentNode)
            currentNode = currentNode.came_from
        path.append(visited_node[0])
        path.reverse()
        return path


"""
Function write_output_to_file converts the matrix back into a graph maze,
and writes outputs to a file.
"""
def write_output_to_file(filename, algorithm_type, output,maze):
    path = []
    with open(filename,"a+") as f:
        f.write("%s\n"%(algorithm_type))
        for i in output:
            maze[i.y-1][i.x-1] = 'P'
        for line in maze:
            for chac in line:
                f.write("%c"%(chac))
            f.write("\n")

    f.close()


'''
Helper function of build_maze
'''
def covert_file_to_matrix(count, line, maze):
    global start, goal
    newline= []
    for i in line:
        if i =='S':
            start = [line.index(i)+1, count]
        elif i=='G':
            goal = [line.index(i)+1, count]
        newline.append(i)
    maze.append(newline)


'''
Function build_maze constructs a matrix from a graph maze
provided by a given file. In the matrix, 1 is X , 0 is _,
and S and G remain the same as they were in the graph maze.
'''
def build_maze(filepath):
    global maze, start, goal
    maze=[]
    start = []
    goal = []

    with open(filepath) as f:
        line = f.readline()
        count=1
        while line:
            maze_line = line.strip()
            covert_file_to_matrix(count, maze_line, maze)
            line = f.readline()
            count += 1


def main():
    build_maze("pathfinding_a.txt")
    greedySearch(maze, start, goal, 'a')
    build_maze("pathfinding_b.txt")
    greedySearch(maze, start, goal, 'b')

    build_maze("pathfinding_a.txt")
    aStarSearch(maze, start, goal, 'a')
    build_maze("pathfinding_b.txt")
    aStarSearch(maze, start, goal, 'b')

main()
