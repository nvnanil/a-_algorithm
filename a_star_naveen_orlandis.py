import numpy as np
import math
import cv2
from math import dist
import time

fourcc = cv2.VideoWriter_fourcc(*'XVID')                    
out = cv2.VideoWriter('w_space.avi', fourcc, 30.0, (600, 250))

#Creating work space
#map = np.ones((250, 600, 3), np.uint8)*255
b_canvas = np.zeros((250,600,3),np.uint8)
width = 600
height = 250

thresh = 0.5
angle_thresh = 30
x_axis = np.arange(0, 600, thresh)
y_axis = np.arange(0, 250, thresh)
theta_grid = np.arange(0, 360, 30)
theta_move = [-60, -30, -0, 30, 60]

####################################Creating obstacle space
def w_space(max_x,max_y):
    #Storing points of the array into an empty list
    all_points = []
    obstacle_space = []
    for i in range(0,max_x):
        for j in range(0,max_y): 
            all_points.append((i,j)) #Appending all points to the list
    for e in all_points:
        x = e[1]
        y = e[0]
    #Storing the points of the obstacle space
    #Defining obstacles using Half - Plane equations
    #Lower rectangle
        if y>=95 and y<=155 and x>=0 and x<=105:
            obstacle_space.append((x,y))
        elif y>=95 and y<=155 and x>=145 and x<=250: #Upper rectangle
            obstacle_space.append((x,y))
        elif x >= 1.75*y - 776.25 and x <= -1.75*y + 1026.25 and y >= 455: #Triangle
            obstacle_space.append((x,y))
        elif (y >= (235 - 5)) and (y <= (365 + 5)) and ((y + 2*x) >= 395) and ((y - 2*x) <= 205) and ((y - 2*x) >= -105) and ((y + 2*x) <= 705): #Hexagon
            obstacle_space.append((x,y))
    return (obstacle_space)

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
            open_dict[(pos, theta)] = get_node(pos, theta, None, np.inf) #Adding key inside key
  open_dict[start_key]['cost'] = 0 #Assigning initial cost to be zero
  return open_dict
################################Goal check
def is_goal(child_node, goal_pos, theta_goal):
    dst = dist(child_node['pos'], goal_pos) #Calculating Euclidean distance
    
    dtheta = np.abs(child_node['theta'] - theta_goal)
    if dst < 1.5 and dtheta <= 30: #Goal reached
        return  True
    else: 
        return False
    
##############################Back tracking
def backtrack(b_node):
    print("Generating path")
    path = []
    while b_node['parent'] is not None:
        path.append(b_node)
        b_node = b_node['parent']
    path.reverse()
    return path

#############################Defining movemnet
def action(node, theta, step):
    x, y = node['pos']
    n_theta = (node['theta'] + theta)%360
    n_theta = np.deg2rad(n_theta)
    x_ = step*np.cos(n_theta) + x
    y_ = step*np.sin(n_theta) + y
    n_pos = ((x_//thresh)//2, (y_//thresh)//2)
    return n_pos, n_theta, node['cost'] + 1

obstacles = w_space(width,height)
###################################Defining workspace
#Puffing Walls
for i in range(5):
    for j in range(b_canvas.shape[0]):
        for k in range(b_canvas.shape[1]):
            b_canvas[j][i] = (0,0,255)
            b_canvas[i][k] = (0,0,255)
            b_canvas[b_canvas.shape[0]-1-i][k] = (0,0,255)
            b_canvas[j][b_canvas.shape[1]-1-i] = (0,0,255)
for c in obstacles: 
    x = c[0]
    y = c[1]
    b_canvas[(x,y)]=[0,0,255] #Coloring the obstacles

ch1, ch2, ch3 = cv2.split(b_canvas)
ch3 = ch3.T
 ###########################Checking if child node in obstacle path
def o_space(pose):
    x = pose[0]
    y = pose[1]
    if ch3[x][y] == 255:
        return False
ip = True    
while ip:

    print("---------------------------------------------------------")
    start_x= int(input("Enter the x coordinate of the start point: "))
    start_y= int(input("Enter the y coordinate of the start ponit: "))
    theta_s = int(input("Enter the orientation of the start point: "))
    goal_x= int(input("Enter the x coordinate of the goal point: "))
    goal_y= int(input("Enter the y coordinate of the goal point: "))
    theta_g= int(input("Enter the orientation of the goal point: "))
    k = int(input("Enter the length of step: "))

    if (theta_s/30 != 0) and theta_s not in range (-60, 61):
        print('Invalid entry')
        print("Try again")
    elif (theta_g/30 != 0) and theta_s not in range (-60, 61):
        print("Invalid entry")
        print("Try again")
    elif k not in range(0,11):
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
    s_node_key = (s_node,theta_s)
    nodes = initial_nodes(s_node)

    def a_star(g_node, theta_g):
        open_dict = {s_node_key: dist(s_node, g_node)}
        c_list = {s_node_key}
        create = [nodes[s_node_key]] #Contains initial information

        while len(open_dict): #Loop until open list is empty
            key = min(open_dict, key = open_dict.get) #Finds the node with the smallest distance
            c_list.add(key)
            open_dict.pop(key)
            m_node = nodes[key]
            if is_goal(m_node, g_node, theta_g):
                print("Goal reached")
                return backtrack(m_node), create
            for t_list in theta_move:
                pos, theta, cost = action(m_node, t_list, k) #New node and cost
            if not o_space(pos) and (pos,theta) not in c_list:
                child = nodes[(pos,theta)]
                if cost < child['cost']:
                    child['cost'] = cost
                    child['parent'] = m_node
                    open_dict[(pos, theta)] = cost + dist(pos, g_node)
                    create.append(child)

            

            





    
    
