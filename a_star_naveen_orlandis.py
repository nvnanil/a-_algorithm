import numpy as np
import math
import cv2 as cv
from math import dist

#Creating workspace
map = np.ones((250, 600, 3), np.uint8)*255
thresh = 0.5
angle_thresh = 30
x_grid = np.arange(0, 400, thresh)
y_grid = np.arange(0, 250, thresh)
theta_grid = np.arange(0, 360, 30)

#Creating nodes and storing in a dictionary
def get_node( pos, theta, parent, cost):
    Node  = {'pos': pos,
             'theta': theta, 
             'parent': parent, 
             'cost': cost}
    return Node

def initial_nodes(start_key):
  open_dict = {}
  for x in x_grid: 
    for y in y_grid:  
        pos = (x, y)
        for theta in theta_grid:  
            open_dict[(pos, theta)] = get_node(pos, theta, None, np.inf)
  open_dict[start_key]['cost'] = 0
  return open_dict

def check_goal(child_node, goal_pos, theta_goal):
    dst = dist(child_node['pos'], goal_pos) #Calculating Euclidean distance
    
    dtheta = np.abs(child_node['theta'] - theta_goal)
    # print(dtheta, child_node['theta'], theta_goal)
    if dst < 1.5 and dtheta <= 30: #Goal reached
        return  True
    else: 
        return False
    
    #Entering the input values
while ip:
    print("---------------------------------------------------------")
    start_x= int(input("Enter the x coordinate of the start point: "))
    start_y= int(input("Enter the y coordinate of the start ponit: "))
    goal_x= int(input("Enter the x coordinate of the goal point: "))
    goal_y= int(input("Enter the y coordinate of the goal point: "))

    if (start_x > b_canvas.shape[1] or start_y > b_canvas.shape[0] or goal_x > b_canvas.shape[1] or goal_y > b_canvas.shape[0]): #Checking whether outside the work space
        print("Invalid input, entered value outside the path space")
        print("Try Agian")
    elif ch3[start_x][start_y] == 255 or ch3[goal_x][goal_y] == 255: #Checking for obstacles
        print("Invalid input, entered value in obstacle space")
        print("Try Again")
    else:
        ip = False