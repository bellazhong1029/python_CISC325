'''
The algorithm uses four global variables, which are 
locations: a list shows locations of all queens on a chessboard
q_in_rows: a list shows total number of queens in each row
q_in_diags: a list shows total number of queens in each diagonal
empty_rows: a list shows which rows are currently empty
'''
import random 
import time

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]

def output_locations(filename):
    global locations
    with open(filename, "a") as f:
        f.write(str(locations)+"\n")

'''
Function init_informed 
takes one argument: size of the chessboard(int), and
initilizes chessboard with informed methods
'''
def init_informed(n: int) -> None:
    
    global locations, q_in_rows, q_in_diags, empty_rows
    
    locations=[0]*n
    q_in_rows=[0]*n
    q_in_diags=[0]*(4*n-2)
    empty_rows=list(range(0,n))
    random.shuffle(empty_rows)
    
    for col in range(0,n):
        best_row=find_best_row(n, col)
        
        #place the queen in the best row
        locations[col]=best_row
        q_in_rows[best_row]+=1
        q_in_diags[col+best_row]+=1
        q_in_diags[3*n+best_row-col-2]+=1
    
'''
Function find_best_row 
takes two parameters: size of the chessboard, postion of a queen, and 
returns an Integer indicating new position of the queen
'''    
def find_best_row(n: int, col: int) -> int:
    global locations, q_in_rows, q_in_diags, empty_rows
    min_confs=n #highest possible value
    rows=[]
    
    r=random.randint(0,len(empty_rows))
    for i in range(r, len(empty_rows)):
        row=empty_rows[i]
        if 0==q_in_diags[col+row]+q_in_diags[3*n+row-col-2]:
            best_row=empty_rows.pop(i)
            return best_row
    for i in range(0, r):
        row=empty_rows[i]
        if 0==q_in_diags[col+row]+q_in_diags[3*n+row-col-2]:
            best_row=empty_rows.pop(i)
            return best_row

    for row in range(0,n):
        conflicts=q_in_rows[row]+q_in_diags[col+row]+q_in_diags[3*n+row-col-2]
        if conflicts<min_confs:
            min_confs=conflicts
            rows=[row]
        if conflicts==min_confs:
            rows.append(row)
    best_row=random.choice(rows)            
    return best_row

'''
Function current_conflicts_of_queen
takes two parameters: size of the chessboard, postion of a queen, and 
returns an Integer indicating the number of total conflicts the queen has
'''
def current_conflicts_of_queen(n: int, col: int) -> int:
    global locations, q_in_rows, q_in_diags
    row=locations[col]
    return q_in_rows[row]+q_in_diags[col+row]+q_in_diags[3*n+row-col-2]-3

'''
Function solution_found
takes one paramter: size of the chessboard, and 
returns a Boolean indicating if a solution is found
'''
def solution_found(n: int) -> bool:
    global q_in_rows, q_in_diags
    
    for row in q_in_rows:
        if not row==1:
            return False
    for diag in q_in_diags:
        if diag>1:
            return False
    return True


'''
Read inputs from file nqueens.txt
with each line n indicates a size of the chessboard(n*n)
'''
input_board_sizes=read_integers("nqueens.txt")
with open("nqueens_out.txt", "w") as f:
        f.write("")
while len(input_board_sizes)>0:
    # Get size of chessboard
    n=input_board_sizes.pop(0)
    
    '''
    Reinitialize chessboard if the steps 
    required to find a solution exceeds max steps
    '''
    max_steps=10000
    inits=0
    solved=False
    while (not solved):
        tic_init=time.time()
        step=0
        
        # Initialize chessboard
        init_informed(n)
        toc_init=time.time()
        inits+=1
        tic_iter=time.time()
        '''
        Iterate queens on the chessborad till a solution 
        is found or steps taken is more than max_steps = 10,000
        '''
        while (step<max_steps and not solved):
            max_confs=-1
            target_queens=[]
           
            # Find all queens with max conflicts on the chessboard
            for queen in range(0,n):
                confs=current_conflicts_of_queen(n, queen)
                if confs>max_confs:
                    max_confs=confs
                    target_queens=[queen]
                if confs==max_confs:
                    target_queens.append(queen)
            '''
            Randomly choose a queen from all the queens that have max conflicts, and
            place the queen to a new position that generates min conflicts 
            '''
            target_queen=random.choice(target_queens)
            best_row=find_best_row(n, target_queen)
           
            # Update chessborad after adjusting
            old_row=locations[target_queen]
            locations[target_queen]=best_row
            q_in_rows[best_row]+=1
            q_in_diags[target_queen+best_row]+=1
            q_in_diags[3*n+best_row-target_queen-2]+=1
            
            q_in_rows[old_row]-=1
            q_in_diags[target_queen+old_row]-=1
            q_in_diags[3*n+old_row-target_queen-2]-=1
            if q_in_rows[old_row]==0:
                empty_rows.append(old_row)
            
            
            step+=1
            solved = solution_found(n)
        toc_iter=time.time()
        '''
        Print out following information:
        size of the chessboard, initilizations taken, steps taken, 
        chessboard initilization time, chessboard adjusting time, total time
        '''
        duration_init=toc_init-tic_init
        duration_iter=toc_iter-tic_iter
        duration_total=duration_iter+duration_init
        print("\n Size: %d Inits: %d Steps %d, init time: %.3f, iter time: %.3f, Time total: %.3f" %(n,inits, step, duration_init, duration_iter, duration_total))
        # Write ouputs to file nqueens_out.txt
        output_locations("nqueens_out.txt")
