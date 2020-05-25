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
    ceil_layers={}
    
    def __init__(self,file_name):
        self.load(file_name)
        self.instance=self
    
    def load(self,file_name):
        #Cargamos el mapa
        self.world_map = tmxreader.TileMapParser().parse_decode(file_name)
        
        for layer in self.world_map.layers:
            if 'level' in layer.properties:
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
            #print ("reading layer:",layer.name)
            if 'level' in layer.properties:
                print ("creating layer:",layer.name)
                h=float(layer.properties['level'])*2
                if layer.properties['tipo'] in tipo:
                    tipo[layer.properties['tipo']](scn_mgr,layer.name,h)
        
        # vamos a registrar las layers necesarias
        for layer in self.world_map.layers:
            if 'tipo' in layer.properties:
                if layer.properties['tipo']=='w':
                    self.wall_layers[int(layer.properties['level'])]=layer
                elif layer.properties['tipo']=='f':
                    self.floor_layers[int(layer.properties['level'])]=layer
                elif layer.properties['tipo']=='c':
                    self.ceil_layers[int(layer.properties['level'])]=layer
                
        
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
                    try:
                        mesh=self.world_map.tiles[gid].properties[self.MESH_PROP]
                    except:
                        mesh="wall.mesh"
                        print("problems with ",gid, "in ",tx,"-",ty)
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                    wall=scn_mgr.createEntity(mesh)
                    wall.setCastShadows(True)
                    wallNode1 = scn_mgr.getRootSceneNode().createChildSceneNode()
                    wallNode2=wallNode1.createChildSceneNode()
                    wallNode2.translate(-.5,0,-.5)
                    try:
                        wallNode1.yaw(Ogre.Ogre.Radian((float(self.world_map.tiles[gid].properties[self.ROT_PROP]))/180*np.pi),Ogre.Node.TS_WORLD)
                    except:
                        pass
                    #wallNode.translate(py+0.5, h, px+0.5)
                    wallNode1.setPosition(px+0.5, h, py+0.5)
                    wallNode2.attachObject(wall)
    
    def makefloor (self,scn_mgr,layername,h):
        x=0
        y=0
        n=0
        while x<self.world_map.width:
            xr=[x,min(x+32,self.world_map.width)]
            while y<self.world_map.height:
                yr=[y,min(y+32,self.world_map.height)]
                self.makefloorrange (scn_mgr,layername,xr,yr,h,n)
                n=n+1
                y=y+32
            y=0
            x=x+32

    def tiletypes (self,layername,xr,yr,h):
        tiles={}
        layer=self.world_map.named_layers[layername]
        for tx in range (xr[0],xr[1]):
            for ty in range (yr[0],yr[1]):
                gid=layer.content2D [tx][ty]
                if not gid==0:
                    if gid in tiles:
                      tiles[gid]+=1
                    else:
                      tiles[gid]=1
        return tiles    
    
    def makefloorrange (self,scn_mgr,layername,xr,yr,h,n):
        tiles=self.tiletypes(layername,xr,yr,h)
        if len(tiles)==0: #no hay nada que dibujar
            return None
        #print ("creating floor",xr,"-",yr,"-n types of tiles:",len(tiles))
        h+=.025
        layer=self.world_map.named_layers[layername]
        man=scn_mgr.createManualObject(layername+str(n))
        #man.estimateIndexCount(ntiles) #Numero de tiles
        #man.estimateVertexCount(ntiles*4) #Numero de vertices
        
        for tiletype in tiles.keys(): #vamos a hacer un submesh por tipo de tile
          if self.MATERIAL_PROP in self.world_map.tiles[tiletype].properties:
            mat_name=self.world_map.tiles[tiletype].properties[self.MATERIAL_PROP]
          else:
            print (self.MATERIAL_PROP, " is not in tile (",tiletype,")")
            mat_name=""
          man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
          n=0
          rot=self.FLOOR_ROT[self.world_map.tiles[tiletype].properties[self.ROT_PROP]]
          for tx in range (xr[0],xr[1]):
            for ty in range (yr[0],yr[1]):
                gid=layer.content2D [tx][ty]
                if gid==tiletype:
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                        
                    # vertice n
                    man.position(px, h, py)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 0)
                    man.textureCoord(rot[0][0],rot[0][1])
                    
                    #vertice n+1
                    man.position(px+self.INCTILE_X, h,py)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 1)
                    man.textureCoord(rot[1][0],rot[1][1])
                    
                    #vertice n+2
                    man.position(px+self.INCTILE_X, h,py+self.INCTILE_Y)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 1)
                    man.textureCoord(rot[2][0],rot[2][1])
                        
                    #vertice n+3
                    man.position(px, h, py+self.INCTILE_Y)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 0)
                    man.textureCoord(rot[3][0],rot[3][1])
                    
                    man.quad(n+3, n+2, n+1, n)
                    n+=4
          man.end()  #termino el submesh
                    
        #termino de dar propiedades al objeto manual y lo pongo en  escena
        man.setCastShadows(False)
        #mesh=man.convertToMesh(layername+str(n))
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        #scn_mgr.destroyManualObject(man)
        mannode.attachObject(man)
        #mannode.attachObject(scn_mgr.createEntity(mesh))
        
    def makeceil (self,scn_mgr,layername,h):
        x=0
        y=0
        n=0
        h=h+self.INCTILE_Z-0.025
        while x<self.world_map.width:
            xr=[x,min(x+32,self.world_map.width)]
            while y<self.world_map.height:
                yr=[y,min(y+32,self.world_map.height)]
                self.makeceilrange (scn_mgr,layername,xr,yr,h,n)
                n=n+1
                y=y+32
            y=0
            x=x+32       
        
    def makeceilrange (self,scn_mgr,layername,xr,yr,h,n):
        tiles=self.tiletypes(layername,xr,yr,h)
        if len(tiles)==0: #no hay nada que dibujar
            return None
        print ("creating ceil",xr,"-",yr,"-n types of tiles:",len(tiles))
        layer=self.world_map.named_layers[layername]
        man=scn_mgr.createManualObject(layername+str(n))
        #man.estimateIndexCount(ntiles) #Numero de tiles
        #man.estimateVertexCount(ntiles*4) #Numero de vertices
        
        for tiletype in tiles.keys(): #vamos a hacer un submesh por tipo de tile
          if self.MATERIAL_PROP in self.world_map.tiles[tiletype].properties:
            mat_name=self.world_map.tiles[tiletype].properties[self.MATERIAL_PROP]
          else:
            print (self.MATERIAL_PROP, " is not in tile (",tiletype,")")
            mat_name=""
          man.begin(mat_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
          n=0
          rot=self.FLOOR_ROT[self.world_map.tiles[tiletype].properties[self.ROT_PROP]]
          for tx in range (xr[0],xr[1]):
            for ty in range (yr[0],yr[1]):
                gid=layer.content2D [tx][ty]
                if gid==tiletype:
                    px=self.INCTILE_X*tx
                    py=self.INCTILE_Y*ty
                        
                    # vertice n
                    man.position(px, h, py)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 0)
                    man.textureCoord(rot[0][0],rot[0][1])
                    
                    #vertice n+1
                    man.position(px+self.INCTILE_X, h,py)
                    man.normal(0, 1, 0)
                    #man.textureCoord(0, 1)
                    man.textureCoord(rot[1][0],rot[1][1])
                    
                    #vertice n+2
                    man.position(px+self.INCTILE_X, h,py+self.INCTILE_Y)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 1)
                    man.textureCoord(rot[2][0],rot[2][1])
                        
                    #vertice n+3
                    man.position(px, h, py+self.INCTILE_Y)
                    man.normal(0, 1, 0)
                    #man.textureCoord(1, 0)
                    man.textureCoord(rot[3][0],rot[3][1])
                    
                    man.quad(n, n+1, n+2, n+3)
                    n+=4
          man.end()  #termino el submesh
                    
        #termino de dar propiedades al objeto manual y lo pongo en  escena
        man.setCastShadows(True)
        #mesh=man.convertToMesh(layername+str(n))
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        #scn_mgr.destroyManualObject(man)
        mannode.attachObject(man)
        #mannode.attachObject(scn_mgr.createEntity(mesh))

#
#
#           ESTUDIO DE LAS COLISIONES
#
#

  
    def wallheight(self,layer,objeto,x,y):
        """ ESTUDIO DE LA COLISION DE LAS WALLS"""
        try: 
            return self.collisiontiles.collisiontypes[layer.content2D [int(x)] [int(y)]] (objeto,x,y)
        except:
            return 0
 
    def wallsheight(self,objeto,x,y,z,offset):
        """ Vamos a comprobar las coliciones con las walls"""
        #si estamos fuera del mapa la altura sera 0
        if y>self.world_map.width-offset or x>self.world_map.height-offset:
            return 0
        
        #primero vemos a ver cual es el layer que corresponde a esa altura
        level=int(z)//2

        #estudio de la colisión con las paredes        
        if level in self.wall_layers:
            layer=self.wall_layers[level]
            return max(self.wallheight(layer,objeto,x+offset,y+offset),
                self.wallheight(layer,objeto,x-offset,y-offset),
                self.wallheight(layer,objeto,x+offset,y-offset),
                self.wallheight(layer,objeto,x-offset,y+offset))+level*2
        else: #No existe la layer, luego no hay colisión
            return (-2.0+level*2)


    def floorheight(self,x,y,z):
        """ Debuelve la altura del suelo de un punto """
        level=int(z)//2
        
        #estudio la altura de los objetos        
        if level in self.wall_layers:
            layer=self.wall_layers[level]
            h=self.wallheight(layer,None,x,y)+level*2
            if h>0:
                return h
        
        #Voy a estudiar el suelo que hay mas cercano
        level=int(z+0.2)//2
        
        #si hay nivel de suelo a ese invel
        try:
            if level in self.floor_layers:
                layer=self.floor_layers[level]
                if layer.content2D [int(x)] [int(y)]==0:
                    return -2.0+level*2
                else:
                    return level*2
            else:
                return -2.0+level*2
        except:
            return 0
    
    def ceilheight(self,x,y,z):
        """ Debuelve la altura del techo de un punto """
        level=int(z)//2
                
        #si hay nivel de techo a ese invel
        if level in self.ceil_layers:
            layer=self.ceil_layers[level]
            try:
                if layer.content2D [int(x)] [int(y)]==0:
                    return 4.0+level*2
                else:
                    return level*2+2.0
            except:
                return 4.0+level*2
        else:
            return 4.0+level*2
    
    def floorsheight(self,x,y,z,offset):
        """ Altura de los suelos en un offset """
        level=int(z+0.2)//2
        
        #si hay nivel de suelo a ese invel
        try:
            if level in self.floor_layers:
                layer=self.floor_layers[level]            
                if not layer.content2D [int(x-offset)] [int(y-offset)]==0:
                    return level*2
                elif not layer.content2D [int(x+offset)] [int(y-offset)]==0:
                    return level*2
                elif not layer.content2D [int(x+offset)] [int(y+offset)]==0:
                    return level*2
                elif not layer.content2D [int(x-offset)] [int(y+offset)]==0:
                    return level*2
                else:
                    return -2.0+level*2
            else:
                return -2.0+level*2
        except:
            return 0

        
