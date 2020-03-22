import math
import sys

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, goal, type):
    """Returns a list of tuples as a path
    from the given start to the given goal in the given maze"""
    # Create start and goal node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    goal_node = Node(None, goal)
    goal_node.g = goal_node.h = goal_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the goal
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
                
            if type == 'a':
                write_output_to_file("pathfinding_a_out.txt", "Greedy", path,maze)
            else:
                write_output_to_file("pathfinding_b_out.txt", "Greedy", path,maze)
            return path[::-1] # Return reversed path


        # Generate children
        children = []
        if type == 'a':
            possible_neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        else:
            possible_neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for new_position in possible_neighbors: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - goal_node.position[0]) ** 2) + ((child.position[1] - goal_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)






'''
Class GreedyNode
'''
class GreedyNode:
    def __init__(self,x,y,priority,came_from=None):
        self.x = x
        self.y = y
        self.priority = priority
        self.came_from = came_from

    '''
    function neighbors returns all the neighbor nodes
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
                if node_value == 0 or node_value == 'G' or node_value == 'S':
                    neighbors.append([nodex+1, nodey+1])
        return neighbors

    def is_node(self,node):
        return self.x == node[0] and self.y == node[1]


'''
Function greedySearch finds a path between the start position and the goal
position using Greedy algorithm.
When type == a, it assumes that the agent can move up, down, left, and right,
but not diagonally. The cost of moving up, down, left, or right is 1.
When type == b, it assumes that the agent can move up, down, left, and right,
and diagonally. The cost of moving up, down, left, right or diagonal is 1.
'''
def greedySearch(maze ,start, goal,type):
    startNode = GreedyNode(start[0], start[1],0)
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

        #searching stops when goal is reached
        if currentNode.is_node(goal):
            break
        for next in currentNode.neighbors(type,maze):
            if next not in visited:
                visited.append(next)
                priority = heuristic(goal, next)
                newNode = GreedyNode(next[0], next[1], priority, currentNode)
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
        for line in range(len(maze)):
            for index in range (len(maze[line])):
                item = maze[line][index]
                if item == 0:
                    maze[line][index] = "_"
                elif item == 1:
                    maze[line][index] = "X"
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
        # obstacle normal block= 1
        if i =='X':
            newline.append(1)
        # non-obstavle normal block = 0
        elif i =='_':
            newline.append(0)
        # start block
        elif i =='S':
            newline.append('S')
            start = [line.index(i)+1, count]
        # goal block
        elif i=='G':
            newline.append('G')
            goal = [line.index(i)+1, count]
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
    astar(maze, start, goal, 'a')
    #greedySearch(maze, start, goal, 'a')
    build_maze("pathfinding_b.txt")
    astar(maze, start, goal, 'b')
    #greedySearch(maze, start, goal, 'b')

main()
