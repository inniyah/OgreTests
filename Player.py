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
    V0=np.array([0, 0], dtype='f')
    #mapa=None
    
    def __init__(self,node):
        """set node as node attached to player"""
        self.node=node
        #self.mapa=Ogretmxmap.tmxmap.instance
        #self.pos=np.array([node.getPosition().x, node.getPosition().z], dtype='f')
        self.pos=np.array([0,0], dtype='f')
        self.z=np.double(0)  #Altura del personaje
        self.hsuelo=self.z
        self.velz=0.0
        self.angle=np.double(0) #Angulo de direccion
        self.direccion=np.array([1, 0], dtype='f')
        self.actdireccion()
        self.keyright=False
        self.keyleft=False
        self.keyup=False
        self.keydown=False
        self.keyjump=False
        self.setpos(0,0,0)

     
    def setpos(self,x,y,z):
        self.pos[0]=x
        self.pos[1]=y
        self.z=np.double(z)
        self.actualizanodo()
    
    def actdireccion(self):
        """ devuelve el vector de direccion correspondiente al angulo """
        if self.angle>2*np.pi:
            self.angle-=2*np.pi
        if self.angle<-2*np.pi:
            self.angle+=2*np.pi

        self.direccion[0]=np.cos(self.angle)
        self.direccion[1]=-np.sin(self.angle) 
    
    def jump(self):
        self.keyjump=True
        
    def actualiza(self,t):
        #Actualiza la posición
        
        if self.keyright:
            self.angle-=t*self.ANGULAR_VEL

            self.actdireccion()
        if self.keyleft:
            self.angle+=t*self.ANGULAR_VEL

            self.actdireccion()
        if self.keyup:
            self.moveifcan(self.direccion*t*self.LINEAL_VEL)

        if self.keydown:
            self.moveifcan(-self.direccion*t*self.LINEAL_VEL)

        if self.keyjump:
            self.keyjump=False
            if self.z==self.hsuelo:
                self.velz=10.0

        #miramos si tenemos que caer
        if self.hsuelo<self.z or self.velz>0:
            self.z+=t*self.velz-0.5*9.81*t
            self.velz-=9.81*t
        if self.hsuelo>self.z:
            self.velz=0
            self.z=self.hsuelo
        else:
            #miro a ver si tenemos que caer
            self.moveifcan(self.V0)


        
        
        #Actualiza el nodo
        self.actualizanodo()
    
    def actualizanodo(self):
        # Actualizo la posición y rotación del nodo
        self.node.resetOrientation()
        self.node.yaw(Ogre.Ogre.Radian(self.angle),Ogre.Ogre.Node.TS_LOCAL)
        self.node.setPosition(float(self.pos[0]), float(self.z), float(self.pos[1]))

    def tilepos(self):
        tp= (int(self.pos[0]),int(self.pos[1]))
        return tp

    def moveifcan(self,direccion):
        
        """ Estudia si se puede mover en esa dirección"""
        #primero voy a ver que longitud tiene la direccion
        self.long=sum(direccion*direccion)
        if self.long>2:
            print ("vector muy grande, lo dividimos") #no hecho aun
        
        self.nextpos=self.pos+direccion
        
        if not self.collision(self.nextpos):
            self.pos=self.nextpos
        else:
            self.nextpos=self.pos+np.array([direccion[0],0])
            if not self.collision(self.nextpos):
                self.pos=self.nextpos
            else:
                self.nextpos=self.pos+np.array([0,direccion[1]])
                if not self.collision(self.nextpos):
                    self.pos=self.nextpos    
            
            
    def collision(self,pos):
        """ Comprueba la colision en el mapa de una posicion
            True no se puede mover a la posición indicada"""
        h=self.mapa.collisiontile(self,pos[0],pos[1],self.z,0.25)
        if h-self.z>0.5:
            return True
        else:
            self.hsuelo=h
            return False

        