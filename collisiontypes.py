#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 22:41:44 2020

@author: arky

se definen los distintos tipos de colisiones del mapa
"""

def solid(objeto,x,y):
    #objeto con el que chocamos y posición del tile en el mapa
    #devuelvo la altura del objeto
    return 2.0

def nocollision(objeto,x,y):
    return -2

def stair1_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy)
def stair1_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy))
def stair1_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx)
def stair1_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx))

def stair2_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+0.5)
def stair2_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+0.5)
def stair2_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+0.5)
def stair2_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+0.5)

def stair3_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+1)
def stair3_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+1)
def stair3_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+1)
def stair3_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+1)

def stair4_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+1.5)
def stair4_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+1.5)
def stair4_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+1.5)
def stair4_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+1.5)

def landing1(objeto,x,y):
    return 0.5

def landing2(objeto,x,y):
    return 1

def landing3(objeto,x,y):
    return 1.5



ROT_DIR={"90":"E","180":"S","270":"O","0":"N"}
COLISION_TYPE = {"NP":solid,"":nocollision,
                 "E1N":stair1_N,"E1S":stair1_S,"E1E":stair1_E,"E1O":stair1_O,
                 "E2N":stair2_N,"E2S":stair2_S,"E2E":stair2_E,"E2O":stair2_O,
                 "E3N":stair3_N,"E3S":stair3_S,"E3E":stair3_E,"E3O":stair3_O,
                 "E4N":stair4_N,"E4S":stair4_S,"E4E":stair4_E,"E4O":stair4_O,
                 "L1":landing1, "L2":landing2, "L3":landing3}

class collision_tiles:
    
    def createtiles(self,tilelist):
        self.collisiontypes={0:COLISION_TYPE[""]}
        
        for gid in tilelist.keys():
            if "Collision" in tilelist[gid].properties:
                colprop=tilelist[gid].properties["Collision"]
                if colprop in COLISION_TYPE:
                    self.collisiontypes[gid]=COLISION_TYPE[colprop]
                else:
                    colprop=tilelist[gid].properties["Collision"] + ROT_DIR[tilelist[gid].properties["RotAngle"]]
                    if colprop in COLISION_TYPE:
                        self.collisiontypes[gid]=COLISION_TYPE[colprop]
                    else:
                        self.collisiontypes[gid]=COLISION_TYPE[""]
            else:
                self.collisiontypes[gid]=COLISION_TYPE[""]
                
                

            
