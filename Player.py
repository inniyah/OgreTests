#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:48:00 2020

@author: arky
"""
import numpy as np
import Ogretmxmap
import Ogre



class Player:
    
    #Define velocidades del personaje
    LINEAL_VEL=5
    ANGULAR_VEL=1
    
    def __init__(self,node):
        """set node as node attached to player"""
        self.node=node
        self.mapa=Ogretmxmap.tmxmap.world_map
        self.pos=np.array([node.getPosition().x, node.getPosition().z], dtype='f')
        self.z=np.double(0)  #Altura del personaje
        self.angle=np.double(0) #Angulo de direccion
        self.direccion=np.array([1, 0], dtype='f')
        self.actdireccion()
        
    def actdireccion(self):
        """ devuelve el vector de direccion correspondiente al angulo """
        if self.angle>2*np.pi:
            self.angle-=2*np.pi
        if self.angle<-2*np.pi:
            self.angle+=2*np.pi

        self.direccion[0]=np.cos(self.angle)
        self.direccion[1]=-np.sin(self.angle)
        print(self.direccion)
    
        
    def rotateright(self,t):
        self.angle-=t*self.ANGULAR_VEL
        self.actdireccion()

    def rotateleft(self,t):
        self.angle+=t*self.ANGULAR_VEL
        self.actdireccion()

    def fordward(self,t):
        self.pos+=self.direccion*t*self.LINEAL_VEL
    
    def backward(self,t):
        self.pos-=self.direccion*t*self.LINEAL_VEL
    
    def actualizanodo(self):
        # Actualizo la posición y rotación del nodo
        self.node.resetOrientation()
        self.node.yaw(Ogre.Ogre.Radian(self.angle),Ogre.Ogre.Node.TS_LOCAL)
        self.node.setPosition(float(self.pos[0]), float(self.z), float(self.pos[1]))

        