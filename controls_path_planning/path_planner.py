"""
    This module is your primary workspace. Add whatever helper functions, classes, data structures, imports... etc here.

    We expect most results will utilize more than just dumping code into the plan_paths()
        function, that just serves as a meaningful entry point.

    In order for the rest of the scoring to work, you need to make sure you have correctly
        populated the Destination.path for each result you produce.
"""
import typing
from queue import PriorityQueue

import numpy as np
from typing import Dict
import math

from map_info import Coordinate, Destination, MapInfo
from score_paths import get_path_length, get_path_risk


class PathPlanner:
    def __init__(self, map_info: MapInfo, destinations: typing.List["Destination"]):
        self.map_info: MapInfo = map_info
        self.destinations: typing.List["Destination"] = destinations

    def plan_paths(self):
        """
        This is the function you should re-write. It is expected to mutate the list of
        destinations by calling each Destination's set_path() with the resulting
        path as an argument.

        The default construction shows this format, and should produce 10 invalid paths.
        """
        for site in self.destinations:
            normal_path = self.generate_path(self.map_info.start_coord, site, 0)
            min_path = normal_path
            min_score = get_path_risk(self.map_info, normal_path) + get_path_length(normal_path)/3
            min_weight = 0
            if not (get_path_risk(self.map_info, normal_path) == 0 or get_path_length(normal_path) >= 50):
                iterations = 25
                for i in range(iterations, 2*iterations+1, 1):
                    w = i/float(iterations)
                    path_array = self.generate_path(self.map_info.start_coord, site, w)
                    path_score = get_path_risk(self.map_info, path_array) + get_path_length(path_array)/3
                    if path_score < min_score and get_path_length(path_array) <= 50:
                        min_score = path_score
                        min_path = path_array
            else:
                print("Path either not risky or max length: " + site.name)
            
            path_coords = [Coordinate(arr[0], arr[1]) for arr in min_path]
            site.set_path(path_coords)
            
            
    # 
    def generate_path(self,start, site, risk_coeff) -> list[tuple[int,int]]:
        """
        Uses a version of the A* pathing algorithm with weights to avoid risk to determine the best path to the site
        """
        current_location = start
        path_array = [(int(current_location[0]),int(current_location[1]))]
        
        while True:
            nodes = self.generate_nodes(current_location, path_array)
            min_f = math.inf
            node_scores = []
            min_node = []
            
            for node in nodes:
                if(node == site.coord):
                    path_array.append(site.coord)
                    found_end = True
                    return path_array
                    
                weight = self.map_info.risk_zones[node]*risk_coeff
                g = math.dist(self.map_info.start_coord, current_location) + math.dist(current_location, node)
                h = math.dist(node, site.coord)
                f = g + h + weight
                node_scores.append(({"node":node,"g":g,"h":h,"f":f}))
                
                if f < min_f:
                    min_f = f
                    min_node = node
             
            min_scores = []
            for score in node_scores:
                if score["f"] == min_f:
                    min_scores.append(score)
                
            min_node = min_scores[0]["node"]
            if len(min_scores) > 1:
                min_h = math.inf
                for score in min_scores:
                    if score["h"] < min_h:
                        min_h = score["h"]
                        min_node = score["node"]
            
            path_array.append(min_node)
            current_location = min_node
    
    
    def generate_nodes(self, current_location, path_array) -> list[("tuple")]:
        """
        Generates a list of usable coordinate nodes for the next element in path
        """
        nodes = []
        for i in range(-1,2):
            for j in range(-1,2):
                if not (i == 0 and j == 0):
                    new_node = (current_location[0] + i, current_location[1] + j)
                    if self.map_info.risk_zones[new_node] != 2 and not self.exists_in_path(new_node, path_array):
                        nodes.append(new_node)
        return nodes
    
    def exists_in_path(self, node, path_array) -> bool:
        """
        Determines if node already exists in existing path
        """
        for pt in path_array:
            if node == pt:
                return True
        return False
        
                
            
            
    
            
            