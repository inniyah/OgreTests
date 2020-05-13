#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:38:18 2020

@author: arky
"""

import tmxreader
import Ogre
#import Ogre.RTShader as OgreRTShader
#import Ogre.Bites as OgreBites
#import os.path
import numpy as np
import collisiontypes

class tmxmap:
    
    world_map=None
    INCTILE_X=1
    INCTILE_Y=1
    INCTILE_Z=2
    layerlist={}
    instance=None
    maxh=0
    meta=[]
    MATERIAL_PROP='Material'
    MESH_PROP='3DMesh'
    ROT_PROP='RotAngle'
    FLOOR_ROT={'0':[(1.0,0.0),(0.0,0.0),(0.0,1.0),(1.0,1.0)],
    '270':[(0.0,0.0),(0.0,1.0),(1.0,1.0),(1.0,0.0)],
    '180':[(0.0,1.0),(1.0,1.0),(1.0,0.0),(0.0,0.0)],
    '90':[(1.0,1.0),(1.0,0.0),(0.0,0.0),(0.0,1.0)]}
    wall_layers={}  #Lista de layers conteniendo las walls por niveles
    floor_layers={}
    
    def __init__(self,file_name):
        self.load(file_name)
        self.instance=self
    
    def load(self,file_name):
        #Cargamos el mapa
        self.world_map = tmxreader.TileMapParser().parse_decode(file_name)
        
        for layer in self.world_map.layers:
            if self.maxh<int(layer.properties['level']):
                self.maxh=int(layer.properties['level'])
            
        print("loaded map:", self.world_map.map_file_name)
        print("tiles used:", self.world_map.width, self.world_map.height)
        print("found '", len(self.world_map.layers), "' layers on this map")
        print("max height:",self.maxh)
    
    def createmap(self,scn_mgr):
        """ Crea el mapa sobre la escena"""
        tipo = {'w':self.makewalls, 'c':self.makeceil, 'f':self.makefloor }

        for layer in self.world_map.layers:
            print ("creating layer:",layer.name)
            h=float(layer.properties['level'])*2
            if layer.properties['tipo'] in tipo:
                tipo[layer.properties['tipo']](scn_mgr,layer.name,h)
        
        # vamos a registrar las layers necesarias
        for layer in self.world_map.layers:
            if layer.properties['tipo']=='w':
                self.wall_layers[int(layer.properties['level'])]=layer
            elif layer.properties['tipo']=='f':
                self.floor_layers[int(layer.properties['level'])]=layer
        
        #creamos las layers de colisiones
        print ("creando colisiones")
        self.collisiontiles=collisiontypes.collision_tiles()
        self.collisiontiles.createtiles(self.world_map.tiles)

        
    
    def makewalls(self,scn_mgr,layername,h):
        layer=self.world_map.named_layers[layername]
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=layer.content2D [tx][ty]
                if gid!=0:
                    mesh=self.world_map.tiles[gid].properties[self.MESH_PROP]
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    wall=scn_mgr.createEntity(mesh)
                    wallNode1 = scn_mgr.getRootSceneNode().createChildSceneNode()
                    wallNode2=wallNode1.createChildSceneNode()
                    wallNode2.translate(-.5,0,-.5)
                    wallNode1.yaw(Ogre.Ogre.Radian((-float(self.world_map.tiles[gid].properties[self.ROT_PROP])+90)/180*np.pi),Ogre.Node.TS_WORLD)
                    #wallNode.translate(py+0.5, h, px+0.5)
                    wallNode1.setPosition(py+0.5, h, px+0.5)
                    wallNode2.attachObject(wall)
    
    
    def makefloor (self,scn_mgr,layername,h):
        layer=self.world_map.named_layers[layername]
        man=scn_mgr.createManualObject(layername)
        man.estimateIndexCount(self.world_map.width*self.world_map.height) #Numero de tiles
        man.estimateVertexCount(self.world_map.width*self.world_map.height*4) #Numero de vertices
        
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=layer.content2D [tx][ty]
                if gid!=0:
                    if self.MATERIAL_PROP in self.world_map.tiles[gid].properties:
                        mat_name=self.world_map.tiles[gid].properties[self.MATERIAL_PROP]
                    else:
                        print (self.MATERIAL_PROP, " is not in tile ",tx,"-",ty,"(",gid,")")
                        mat_name=""
                    rot=self.FLOOR_ROT[self.world_map.tiles[gid].properties[self.ROT_PROP]]
                    man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    man.position(py, h, px)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 0)
                    man.textureCoord(rot[0][0],rot[0][1])
                    
                    man.position(py, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 1)
                    man.textureCoord(rot[1][0],rot[1][1])
                    
                    man.position(py+self.INCTILE_Y, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 1)
                    man.textureCoord(rot[2][0],rot[2][1])
                    
                    man.position(py+self.INCTILE_Y, h, px)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 0)
                    man.textureCoord(rot[3][0],rot[3][1])
                    
                    man.quad(0, 1, 2, 3)
                    man.end()
        man.setCastShadows(False)
        #man.convertToMesh("mapa")
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.attachObject(man)
    
    def makeceil (self,scn_mgr,layername,h):
        h=h+self.INCTILE_Z-0.05
        layer=self.world_map.named_layers[layername]
        man=scn_mgr.createManualObject(layername)
        man.estimateIndexCount(self.world_map.width*self.world_map.height) #Numero de tiles
        man.estimateVertexCount(self.world_map.width*self.world_map.height*4) #Numero de vertices
        
        for tx in range (0,self.world_map.width):
            for ty in range (0,self.world_map.height):
                gid=layer.content2D [tx][ty]
                if gid!=0:
                    if self.MATERIAL_PROP in self.world_map.tiles[gid].properties:
                        mat_name=self.world_map.tiles[gid].properties[self.MATERIAL_PROP]
                    else:
                        print (self.MATERIAL_PROP, " is not in tile ",tx,"-",ty,"(",gid,")")
                        mat_name=""
                    rot=self.FLOOR_ROT[self.world_map.tiles[gid].properties[self.ROT_PROP]]
                    man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    man.position(py, h, px)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 0)
                    man.textureCoord(rot[0][0],rot[0][1])
                    
                    man.position(py, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 1)
                    man.textureCoord(rot[1][0],rot[1][1])
                    
                    man.position(py+self.INCTILE_Y, h, px+self.INCTILE_X)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 1)
                    man.textureCoord(rot[2][0],rot[2][1])
                    
                    man.position(py+self.INCTILE_Y, h, px)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 0)
                    man.textureCoord(rot[3][0],rot[3][1])
                    
                    man.quad(3, 2, 1, 0)
                    man.end()                

        #man.setCastShadows(False)
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.attachObject(man)

#
#
#           ESTUDIO DE LAS COLISIONES
#
#

  
    def collisionwall(self,layer,objeto,x,y):
        """ ESTUDIO DE LA COLISION DE LAS WALLS"""
        return self.collisiontiles.collisiontypes[layer.content2D [int(y)] [int(x)]] (objeto,x,y)
        
 
    def collisiontile(self,objeto,x,y,z,offset):
        """ Comprobamos si se puede estar en un tile"""
        
        #si estmos fuera del mapa la altura sera 0
        if y>self.world_map.width-offset or x>self.world_map.height-offset:
            return 0
        
        #primero vemos a ver cual es el layer que corresponde a esa altura
        level=int(z)//2

        #estudio de la colisión con las paredes        
        if level in self.wall_layers:
            layer=self.wall_layers[level]
            h= max(self.collisionwall(layer,objeto,x+offset,y+offset),
                self.collisionwall(layer,objeto,x-offset,y-offset),
                self.collisionwall(layer,objeto,x+offset,y-offset),
                self.collisionwall(layer,objeto,x-offset,y+offset))+level*2
        else: #No existe la layer, luego no hay colisión
            h= -2.0+level*2

        if h>level*2:
            print ("2-"+str(h))
            return h

        #estudio la colisión con el suelo
        level=int(z+0.2)//2
        if level==0:
            return 0
        print (level)
        
        if level in self.floor_layers:
            layer=self.floor_layers[level]
            if layer.content2D [int(y)] [int(x)]==0:
                return -2.0+level*2
            else:
                return level*2
        else:
            return -2.0+level*2
        
    
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