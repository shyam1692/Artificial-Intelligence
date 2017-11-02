#!/usr/bin/env python3
#"""
#Created on Sat Sep  9 17:37:22 2017

#@author: David Crandall, Updated by Shyam Narasimhan
#""All work done here is done on my own"

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board,problem_type,x_unavailable,y_unavailable):    
   N=len(board)
   u=[]
   for i in list(range(0,N)):
       t=[]
       for j in list(range(0,N)):
           if board[i][j]==1 and problem_type=="nrook":
               t.append("R")
           elif board[i][j]==1 and problem_type=="nqueen":
               t.append("Q")
           elif i==x_unavailable-1 and j==y_unavailable-1:
               t.append("X")
           else:
               t.append("_")
       u.append(t)
    
   return ("\n".join([" ".join([col for col in row]) for row in u]))

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]


#Checking if there are pieces present diagonally above from a given position on the board
def diagonalsum(x,r,c,problem_type):
  if problem_type=="nrook":
     return 0==0
  elif problem_type=="nqueen":
     N=len(x)
     y=0
     i=r
     j=c
     while i in list(range(0,N)) and j in list(range(0,N)):
         y=y+ x[i][j]
         i=i-1
         j=j+1      
     i=r
     j=c
     while i in list(range(0,N)) and j in list(range(0,N)):
         y=y+ x[i][j]
         i=i-1
         j=j-1
      
     return y==0


# Get list of successors of given board state, checking conditions
def successors(board,problem_type):    
    x=[]
    for r in range(0,N):
        if sum(board[r])>0:
            continue
        for c in range(0,N):
            if sum( [ row[c] for row in board ] )>0 or\
            diagonalsum(board,r,c,problem_type)==False or\
            (r==(x_unavailable-1) and c==(y_unavailable-1)):
                continue           
            x.append(add_piece(board,r,c))
        if len(x)>0 or sum(board[r])==0:
            break
    return x


# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N 


#Solve
def solve(initial_board,problem_type):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop(),problem_type ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False


#problem_type is if nqueen or nrook
#N is the size of the board (NxN)
#x_unavailable and y_unavailable are the coordinates of unavailable square in board
problem_type= sys.argv[1]
N = int(sys.argv[2])
x_unavailable=int(sys.argv[3])
y_unavailable=int(sys.argv[4])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
solution = solve(initial_board,problem_type)
print (printable_board(solution,problem_type,x_unavailable,y_unavailable) if solution else "Sorry, no solution found. :(")