#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:38:18 2020

@author: arky
"""

import tmxreader
import Ogre
import Ogre.RTShader as OgreRTShader
import Ogre.Bites as OgreBites
import os.path

class tmxmap:
    def __init__(self):
        self.INCTILE_X=20
        self.INCTILE_Y=20
    
    def load(self,file_name):
        self.world_map = tmxreader.TileMapParser().parse_decode(file_name)
        print("loaded map:", self.world_map.map_file_name)
        print("tiles used:", self.world_map.width, self.world_map.height)
        print("found '", len(self.world_map.layers), "' layers on this map")
    
    def makefloor (self,scn_mgr,layernumber):
        
        man=scn_mgr.createManualObject("test")
                #Para hacer el objeto dianico, por defecto False
        man.estimateIndexCount(self.world_map.width*self.world_map.height) #Numero de tiles
        man.estimateVertexCount(self.world_map.width*self.world_map.height*4) #Numero de vertices
        
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=self.world_map.layers[layernumber].content2D [tx][ty]
                mat_name=self.world_map.tiles[gid].properties['material']
                man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
                px=self.INCTILE_X*tx
                py=self.INCTILE_Y*ty
                man.position(py, 0, px)
                man.normal(0, 1, 0)
                man.textureCoord(0, 0)
                man.position(py, 0, px+self.INCTILE_X)
                man.normal(0, 1, 0)
                man.textureCoord(0, 1)
                man.position(py+self.INCTILE_Y, 0, px+self.INCTILE_X)
                man.normal(0, 1, 0)
                man.textureCoord(1, 1)
                man.position(py+self.INCTILE_Y, 0, px)
                man.normal(0, 1, 0)
                man.textureCoord(1, 0)
                man.quad(0, 1, 2, 3)
                man.end()                
        
        #man.end()
        return man