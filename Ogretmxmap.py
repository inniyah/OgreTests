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
    
    world_map=None
    INCTILE_X=1
    INCTILE_Y=1
    layerlist={}
    
    def __init__(self,file_name):
        self.load(file_name)
    
    def load(self,file_name):
        self.world_map = tmxreader.TileMapParser().parse_decode(file_name)
        for layer in self.world_map.layers:
            self.layerlist[layer.name]=int(layer.id)-1
            
        print("loaded map:", self.world_map.map_file_name)
        print("tiles used:", self.world_map.width, self.world_map.height)
        print("found '", len(self.world_map.layers), "' layers on this map")
    
    def makewalls(self,scn_mgr,layername,h):
        layernumber=self.layerlist[layername]
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=self.world_map.layers[layernumber].content2D [tx][ty]
                if gid!=0:
                    mesh=self.world_map.tiles[gid].properties['mesh']
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    wall=scn_mgr.createEntity(mesh)
                    wallNode = scn_mgr.getRootSceneNode().createChildSceneNode()
                    wallNode.attachObject(wall)
                    wallNode.setPosition(py, h, px)

    
    
    def makefloor (self,scn_mgr,layername,h):
        layernumber=self.layerlist[layername]
        man=scn_mgr.createManualObject(layername)
        man.estimateIndexCount(self.world_map.width*self.world_map.height) #Numero de tiles
        man.estimateVertexCount(self.world_map.width*self.world_map.height*4) #Numero de vertices
        
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=self.world_map.layers[layernumber].content2D [tx][ty]
                if gid!=0:
                    mat_name=self.world_map.tiles[gid].properties['material']
                    man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    man.position(py, h, px)
                    man.normal(0, 1, 0)
                    man.textureCoord(0, 0)
                    
                    man.position(py, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    man.textureCoord(0, 1)
                    
                    man.position(py+self.INCTILE_Y, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    man.textureCoord(1, 1)
                    
                    man.position(py+self.INCTILE_Y, h, px)
                    man.normal(0, 1, 0)
                    man.textureCoord(1, 0)
                    
                    man.quad(0, 1, 2, 3)
                    man.end()
        man.setCastShadows(False)
        #man.convertToMesh("mapa")
        return man
    
    def makeceil (self,scn_mgr,layername,h):
        layernumber=self.layerlist[layername]
        man=scn_mgr.createManualObject(layername)
        man.estimateIndexCount(self.world_map.width*self.world_map.height) #Numero de tiles
        man.estimateVertexCount(self.world_map.width*self.world_map.height*4) #Numero de vertices
        
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=self.world_map.layers[layernumber].content2D [tx][ty]
                if gid!=0:
                    mat_name=self.world_map.tiles[gid].properties['material']
                    man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    man.position(py, h, px)
                    man.normal(0, -1, 0)
                    man.textureCoord(0, 0)

                    man.position(py, h, px+self.INCTILE_X)
                    man.normal(0, -1, 0)
                    man.textureCoord(0, 1)

                    man.position(py+self.INCTILE_Y, h, px+self.INCTILE_X)
                    man.normal(0, -1, 0)
                    man.textureCoord(1, 1)

                    man.position(py+self.INCTILE_Y, h, px)
                    man.normal(0, -1, 0)
                    man.textureCoord(1, 0)
                
                    man.quad(3, 2, 1, 0)
                    man.end()                

        #man.setCastShadows(False)
        return man
    
    def metadata(self,layername,x,y):
        layernumber=self.layerlist[layername]
        gid=self.world_map.layers[layernumber].content2D [x][y]
        if gid!=0:
            ret=self.world_map.tiles[gid].properties['tipo']
        else:
            ret=0
        
        return ret