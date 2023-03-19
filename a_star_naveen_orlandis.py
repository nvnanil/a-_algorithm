import numpy as np
import math
import cv2 as cv
from math import dist
import time

#Map Space
map = np.ones((250, 600, 3), np.uint8)*255
thresh = 0.5
angle_thresh = 30
x_axis = np.arange(0, 600, thresh)
y_axis = np.arange(0, 250, thresh)
theta_grid = np.arange(0, 360, 30)
###################################Defining workspace
b_canvas = np.zeros((250,600,3),np.uint8)
#Puffing Walls
for i in range(5):
    for j in range(b_canvas.shape[0]):
        for k in range(b_canvas.shape[1]):
            b_canvas[j][i] = (0,0,255)
            b_canvas[i][k] = (0,0,255)
            b_canvas[b_canvas.shape[0]-1-i][k] = (0,0,255)
            b_canvas[j][b_canvas.shape[1]-1-i] = (0,0,255)

####################################Creating nodes and storing in a dictionary
def get_node( pos, theta, parent, cost):
    Node  = {'pos': pos,
             'theta': theta, 
             'parent': parent, 
             'cost': cost}
    return Node

def initial_nodes(start_key):
  open_dict = {}
  for x in x_axis: 
    for y in y_axis:  
        pos = (x, y)
        for theta in theta_grid:  
            open_dict[(pos, theta)] = get_node(pos, theta, None, np.inf)
  open_dict[start_key]['cost'] = 0 #Assigning initial cost to be zero
  return open_dict
################################Goal check
def check_goal(child_node, goal_pos, theta_goal):
    dst = dist(child_node['pos'], goal_pos) #Calculating Euclidean distance
    
    dtheta = np.abs(child_node['theta'] - theta_goal)
    if dst < 1.5 and dtheta <= 30: #Goal reached
        return  True
    else: 
        return False
    
while ip:

    print("---------------------------------------------------------")
    start_x= int(input("Enter the x coordinate of the start point: "))
    start_y= int(input("Enter the y coordinate of the start ponit: "))
    theta_s = int(input("Enter the orientation of the start point: "))
    goal_x= int(input("Enter the x coordinate of the goal point: "))
    goal_y= int(input("Enter the y coordinate of the goal point: "))
    theta_g= int(input("Enter the orientation of the goal point: "))
    K = int(input("Enter the length of step: "))

    if (theta_s/30 != 0) and theta_s not in range (-60, 61):
        print('Invalid entry')
        print("Try again")
    elif (theta_g/30 != 0) and theta_s not in range (-60, 61):
        print("Invalid entry")
        print("Try again")
    elif K not in range(0,11):
        print("Enter K in the range of 1 to 10; Try again")
    if (start_x > b_canvas.shape[1] or start_y > b_canvas.shape[0] or goal_x > b_canvas.shape[1] or goal_y > b_canvas.shape[0]): #Checking whether outside the work space
        print("Invalid input, entered value outside the path space")
        print("Try Agian")
    elif ch3[start_x][start_y] == 255 or ch3[goal_x][goal_y] == 255: #Checking for obstacles
        print("Invalid input, entered value in obstacle space")
        print("Try Again")
    else:
        ip = False
    
    s_node = (start_x,start_y)
    g_node = (goal_x, goal_y)
    s_node_ = (s_node,theta_s)
    nodes = initial_nodes(s_node)

    
    
