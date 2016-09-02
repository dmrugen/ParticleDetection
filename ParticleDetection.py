# -*- coding: utf-8 -*-
"""
Author: Mrugen Anil Deshmukh (mad5js)
Date Created: 24 April 2016
"""
import time
t1 = time.clock()
from collections import namedtuple
from matplotlib import pyplot as plt

# Read in the table of image values. 'data' is a 2d list with the values stored in it
txt = open('bigPart.txt')
d1 = txt.read().split('\n')
data = []
for i in range(len(d1)):
    d = d1[i].split(' ')
    for da in range(len(d)):
        if d[da]=='':
            del(d[da])
        else:
            d[da]=int(d[da])
    data.append(d)

# I have used namedtuples here to use the x (column number) and y (row number) for every value while plotting the scatter plot
point = namedtuple('point', ['d','y','x'])
par = []
for i in range(len(data)):
    pa=[]
    for j in range(len(data[i])):
        pa.append(point(data[i][j],i,j))
    par.append(pa)


# I am using the Breadth First Search algorithm where I treat every particle cluster as a tree
# db is a dictionary with the earliest value occuring in the data as the vertex and the value being a set of all the values attached to it
# Have used the namedtuples here to use them while plotting later
db = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j]==1:
            p = set()            
            try:
                if par[i][j+1].d==1:                   
                    p.add(par[i][j+1])
            except IndexError:
                pass
            try:
                if par[i+1][j].d==1:                    
                    p.add(par[i+1][j])
            except IndexError:
                pass
            try:
                if par[i][j-1].d==1:
                    if j == 0:
                        pass
                    else:                        
                        p.add(par[i][j-1])
            except IndexError:
                pass
            try:
                if par[i-1][j].d==1:
                    if i == 0:
                        pass
                    else:
                        p.add(par[i-1][j])
            except IndexError:
                pass                    
            
            db[par[i][j]] = p
        else:
            pass

# Following function returns the set of all the values in a cluster, given its vertex (earliest occuring point)
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

# Following loop used to determine all the clusters present in the data
# 'clusters' is a list of sets of all the clusters (particles)
clusters = []
for ia in range(len(data)):
    for ib in range(len(data[ia])):
        if data[ia][ib] == 1:
            xa = bfs(db,par[ia][ib])
            clusters.append(xa)
            m = list(xa)
            for n in range(len(m)):
                try:
                    # After a cluster is determined and added to the list, change the values
                    # to avoid getting the same cluster again
                    # otherwise, for n elements in a cluster we get the same cluster n times
                    data[m[n].y][m[n].x] = 2
                except IndexError:
                    pass
print("Total number of particles is:",len(clusters))

# Following functions deals with plotting a scatter plot
def ScatterPlot(cluster):
    x=[]
    y=[]
    colcount=1
    colors=[]
    for i in range(len(cluster)):
        for j in cluster[i]:
            x.append(j.x)
            y.append(j.y)
            colors.append(colcount)
        colcount+=1   
    plt.figure(figsize=(10,10))
    plt.scatter(x,y,c=colors)
    plt.title('Scatter plot of the image data')
    plt.xlabel('Column number (x)')
    plt.ylabel('Row number (y)')
    
ScatterPlot(clusters)
t3 = time.clock()
print("Execution time (in ms):", (t3-t1)*1000)
