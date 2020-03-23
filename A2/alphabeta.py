class node:
    """
    A Node for a tree that can have any number of children. Node is either of type
    MAX, MIN, or leaf. Only leaf nodes have values. 
    """
    def __init__(self, node_type):
        self.children=[]
        
        if node_type=="MAX":
            self.is_max=True
            self.is_min=False
            self.is_leaf=False
            
        elif node_type=="MIN":
            self.is_max=False
            self.is_min=True
            self.is_leaf=False
            
        else: #is leaf
            self.is_max=False
            self.is_min=False
            self.is_leaf=True
            self.val=int(node_type)
        
def alpha_beta(cur_node, alpha, beta):
    """
    Performs minimax on a tree with alpha-beta-pruning. Should be called with
    (root, -inf, +inf).
    """
    if cur_node.is_leaf: #if leaf we return static evaluation of leaf
        global nr_leafs_visited
        nr_leafs_visited+=1
        return cur_node.val
    
    if cur_node.is_max:
        best_val=-10_000_000
        for child in cur_node.children:
            best_val=max(best_val, alpha_beta(child, alpha, beta))
            alpha=max(alpha, best_val)
            
            if alpha>=beta:
                break
        return best_val
        
    if cur_node.is_min:
        best_val=10_000_000
        for child in cur_node.children:           
            best_val=min(best_val, alpha_beta(child, alpha, beta))
            beta=min(beta, best_val)
            
            if alpha>=beta:
                break
        return best_val
    
def read_input_file(filename):
    """
    Reads a text file and returns all lines in a list.
    """
    with open(filename) as f:
        lines=f.readlines()
    return lines
     

def input_to_tree(line):   
    """
    Takes a string of correct format and returns the root of the tree
    represented by that string. Assumes correct format.
    """   
    import re 
    tree={}
    
    #fetch list ["A","B","C","D","E","F"] from "{(A,B)} {(C,D),(E,F)} etc.
    line=re.findall(r"\(([A-Za-z0-9_]+),([A-Za-z0-9_]+)\)", line) 
    
    for pair in line:
        if pair[1]=="MAX" or pair[1]=="MIN": #create a new node
            n=node(pair[1])
            if len(tree)==0: #then root of tree
                root=n
            tree[pair[0]]=n
        elif pair[1].isdigit(): #is then a leaf node
            tree[pair[0]].children.append(node(pair[1]))
        else: #add as a child
            tree[pair[0]].children.append(tree[pair[1]])
    
    return root


def write_output_to_file(filename, output, index):
    """
    Writes outpus to a file.
    """
    with open(filename,"a+") as f:
        f.write("Graph"+str(index)+": " + output) 
    f.close()

        
lines=read_input_file("alphabeta.txt")
index = 0
while len(lines)>0:
    index += 1
    line=lines.pop(0)
    if len(line)>1: #not a blankspace
        root=input_to_tree(line)
        nr_leafs_visited=0
        best_val=alpha_beta(root, -10_000_000, 10_000_000)
        output = "Best possible value: %d; Number of leafs visited %d\n" %(best_val, nr_leafs_visited)
        write_output_to_file("alphabeta_out.txt",output,index)
        