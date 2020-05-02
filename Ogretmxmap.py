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
    INCTILE_Z=2
    layerlist={}
    instance=None
    maxh=0
    layerlist={}
    meta=[]    
    
    def __init__(self,file_name):
        self.load(file_name)
        self.instance=self
    
    def load(self,file_name):
        #Cargamos el mapa
        self.world_map = tmxreader.TileMapParser().parse_decode(file_name)
        #Hacemos el listado de las capas y de las metadatas
        for layer in self.world_map.layers:
            if self.maxh<int(layer.properties['level']):
                self.maxh=int(layer.properties['level'])
            self.layerlist[layer.name]=int(layer.id)-1
        #Hacemos el listado de las metadatas
        self.metalayer=[None for i in range(0,self.maxh+1)]
        for layer in self.world_map.layers:
            if layer.properties['tipo']=='m':
                self.metalayer[int(layer.properties['level'])]=layer
            
        print("loaded map:", self.world_map.map_file_name)
        print("tiles used:", self.world_map.width, self.world_map.height)
        print("found '", len(self.world_map.layers), "' layers on this map")
        print("max height:",self.maxh)
    
    def createmap(self,scn_mgr):
        """ Crea el mapa sobre la escena"""
        tipo = {'w':self.makewalls, 'c':self.makeceil, 'f':self.makefloor }

        for layer in self.world_map.layers:
            h=float(layer.properties['level'])*2
            if layer.properties['tipo'] in tipo:
                tipo[layer.properties['tipo']](scn_mgr,layer.name,h)
    
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
        man=scn_mgr.createManualObject("floor")
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
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.attachObject(man)
    
    def makeceil (self,scn_mgr,layername,h):
        h=h+self.INCTILE_Z
        layernumber=self.layerlist[layername]
        man=scn_mgr.createManualObject("ceil")
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
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.attachObject(man)
    
    def collisiontile(self,x,y,z,offset):
        """ Comprobamos si se puede estar en un tile"""
        #primero vemos a ver cual es el layer que corresponde a esa altura
        layer=self.metalayer[int(z//2)]
        
        if (layer.content2D [int(y+0.5)] [int(x+0.5)]!=0 or
            layer.content2D [int(y-0.5)] [int(x-0.5)]!=0 or
            layer.content2D [int(y+0.5)] [int(x-0.5)]!=0 or
            layer.content2D [int(y-0.5)] [int(x+0.5)]!=0):
            return True
        else:
            return False
        

    
    def metadata(self,layername,x,y):
        # Comporbamos no pasarnos de los limites del mapa
        if y>self.world_map.width-1 or x>self.world_map.height-1:
            return 0
        layernumber=self.layerlist[layername]
        gid=self.world_map.layers[layernumber].content2D [y][x]
#        if gid!=0:
#            ret=self.world_map.tiles[gid].properties['tipo']
#        else:
#            ret=0
        
        return gid