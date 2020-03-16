import math

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


def astar(maze, start, goal):
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
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
        # , (-1, -1), (-1, 1), (1, -1), (1, 1) for diagonal

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
class GreedyNode
'''
class GreedyNode:
    def __init__(self,x,y,came_from=None):
        self.x = x
        self.y = y
        self.came_from = came_from

    def neighbors(self):
        global maze
        all_possible_neighbors = []
        neighbors = []
        x = self.x
        y = self.y
        all_possible_neighbors += [[x-1,y], [x+1,y], [x,y-1],[x,y+1]] 
        for node in all_possible_neighbors:
            #node is in maze boundaries
            nodex = node[0] - 1
            nodey = node[1] - 1
            if nodex > 0 and nodey > 0: 
                node_value = maze[nodey][nodex]
                if node_value == 0:
                    neighbors.append([nodex+1, nodey+1])
        return neighbors

        
'''
function greedySearch_a
finds a path between the start position and the goal position using 
Greedy algorithm assuming that the agent can move up, down, left, and right, 
but not diagonally. Further assume that the cost of moving up, down, left, 
or right is 1.
'''
def g(maze ,start, goal):
    frontier = []
    startNode = GreedyNode(start[0], start[1])
    frontier.append(startNode)
    visited = []
    visited.append(start)

    while len(frontier)!=0:
        currentNode = frontier.pop()
        if currentNode.x == goal[0] and currentNode.y == goal[1]:
            break
        for next in currentNode.neighbors():
            if next not in visited:
                priority = greedy_heuristic(goal, next) 


def greedy_heuristic(goal, next):
    return math.sqrt(math.pow(abs(goal[0] - next[0]),2) + math.pow(abs(goal[1]-next[1]),2)) 
    

def convert_list_to_maze(count, line, maze):
    '''
    convert graph maze into maze of numbers 
    '''
    global start, goal 
    newline= []
    for i in line:
        # obstacle = 1
        if i =='X':
            newline.append(1)
        # non-obstavle = 0
        elif i =='_':
            newline.append(0)
        elif i =='S':
            newline.append(0)
            start = [line.index(i)+1, count]
        elif i=='G':
            newline.append(0)
            goal = [line.index(i)+1, count]
    maze.append(newline)


def main():
    global maze, start, goal
    maze=[]
    start = []
    goal = []

    filepath = "pathfinding_a.txt"
    with open(filepath) as f:
        line = f.readline()
        count=1
        while line:
            maze_line = line.strip()
            convert_list_to_maze(count, maze_line, maze)
            line = f.readline()
            count += 1

    g(maze, start, goal)
    # path = astar(maze, start, goal)
    # print(path)

main()
