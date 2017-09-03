#!/usr/bin/env python

from enum import *
from tkinter import *

class QuadTree:
    "Quadtree"
   
    class Tag(Enum):
        NONE = 0
        SELECTED = 1
        NEIGHBOR = 2
    
    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3
    
    class Direction(Enum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3
        N = 4
        S = 5
        W = 6
        E = 7

    Colors = {Tag.NONE : "#808080", Tag.NEIGHBOR : "#ee3030", Tag.SELECTED : "#30ee30"}
        
    def __init__(self, children=None):
        self.parent = None
        self.children = []
        self.tag = self.Tag.NONE

        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, child):
        assert isinstance(child, QuadTree)
        child.parent = self
        self.children.append(child)
        
    def is_leaf(self):
        return not self.children
                             
    def get_neighbor_of_greater_or_same_size(self, direction):   
        if direction == self.Direction.N:       
            if self.parent is None:
                return None
            if self.parent.children[self.Child.SW] == self:
                return self.parent.children[self.Child.NW]
            if self.parent.children[self.Child.SE] == self:
                return self.parent.children[self.Child.NE]
                
            node = self.parent.get_neighbor_of_greater_or_same_size(direction)            
            if node is None or node.is_leaf():
                return node
                
            return (node.children[self.Child.SW]
                    if self.parent.children[self.Child.NW] == self
                    else node.children[self.Child.SE])
        else:
            # TODO: implement me (symmetric to NORTH case)
            assert False
            return []

    def find_neighbors_of_smaller_size(self, neighbor, direction):   
        candidates = [] if neighbor is None else [neighbor]
        neighbors = []
    
        if direction == self.Direction.N:
            while len(candidates) > 0:
                if candidates[0].is_leaf():
                    neighbors.append(candidates[0])
                else:
                    candidates.append(candidates[0].children[self.Child.SW])
                    candidates.append(candidates[0].children[self.Child.SE])
                    
                candidates.remove(candidates[0])
        else:
            # TODO: implement me (symmetric to NORTH case)
            assert False
            
        return neighbors
            
    def get_neighbors(self, direction):   
        neighbor = self.get_neighbor_of_greater_or_same_size(direction)
        neighbors = self.find_neighbors_of_smaller_size(neighbor, direction)
        return neighbors
            
    def draw(self, canvas, x0, y0, x1, y1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.Colors[self.tag])
        
        if len(self.children) == 4:
            hw = (x1-x0)/2
            hh = (y1-y0)/2
            assert hw > 0
            assert hh > 0
            self.children[self.Child.NW].draw(canvas, x0,    y0,    x0+hw, y0+hh)
            self.children[self.Child.NE].draw(canvas, x0+hw, y0,    x1,    y0+hh)
            self.children[self.Child.SW].draw(canvas, x0,    y0+hh, x0+hw, y1)
            self.children[self.Child.SE].draw(canvas, x0+hw, y0+hh, x1,    y1)
         
posX = 10
posY = 50

def clear_tags_in_quadtree(tree):
    tree.tag = tree.Tag.NONE

    if tree.children is not None:
        for child in tree.children:
            clear_tags_in_quadtree(child)
          
def test_neighbor_finding(tree, selected, direction, canvas):
    clear_tags_in_quadtree(tree)
    selected.tag = tree.Tag.SELECTED
    neighbors = selected.get_neighbors(direction)
    
    for neighbor in neighbors:
        assert neighbor.tag == tree.Tag.NONE
        neighbor.tag = tree.Tag.NEIGHBOR
        
    global posX, posY
    tree.draw(canvas, posX, posY, posX+100, posY+100)
    posX += 10+100;
            
def test_simple_cases():
    tree = QuadTree([QuadTree(),
                     QuadTree([QuadTree(), QuadTree(), QuadTree(), QuadTree()]),
                     QuadTree([QuadTree(), QuadTree(), QuadTree(), QuadTree()]),
                     QuadTree()])
                   
    test_neighbor_finding(tree, tree.children[tree.Child.NW], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.NE].children[tree.Child.NW], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.NE].children[tree.Child.NE], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.SW], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.SE], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.NW], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.NE], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SE], tree.Direction.N, canvas)
    
    global posX, posY
    posX = 10
    posY += 10+100;

def test_complex_cases():
    tree = QuadTree([QuadTree([QuadTree(), QuadTree(), QuadTree(), QuadTree()]),
                     QuadTree([QuadTree(), QuadTree(), QuadTree([QuadTree(), QuadTree(), QuadTree(), QuadTree()]), QuadTree()]),
                     QuadTree([QuadTree(), QuadTree([QuadTree(), QuadTree(), QuadTree(), QuadTree()]), QuadTree(), QuadTree()]),
                     QuadTree()])
                   
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.NW], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SE], tree.Direction.N, canvas)
    test_neighbor_finding(tree, tree.children[tree.Child.SW].children[tree.Child.NE].children[tree.Child.NW], tree.Direction.N, canvas)
    return
    
# Main starts here
            
master = Tk()
master.title("Find neighbors in a Quadtree")
canvas = Canvas(master, width=900, height=600)
canvas.pack()
canvas.create_text(10, 5, text="Selected", fill=QuadTree.Colors[QuadTree.Tag.SELECTED], anchor=NW)
canvas.create_text(10, 20, text="Neighbors", fill=QuadTree.Colors[QuadTree.Tag.NEIGHBOR], anchor=NW)
test_simple_cases()
test_complex_cases()
mainloop()



# - Finding neighbors of greater or equal size is relatively easy
# - Finding neighbors of smaller size is hard, because we have to keep track of how to climb down the tree to find the right neighbors
# - 