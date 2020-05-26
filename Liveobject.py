#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:48:00 2020

@author: arky
"""
import numpy as np
import Ogretmxmap
import Ogre



class LiveObject(object):
    
    #Define velocidades del personaje
    LINEAL_VEL=5
    ANGULAR_VEL=1
    V0=np.array([0, 0], dtype='f')
    
    def __init__(self,node):
        """set node as node attached to object"""
        self.node=node
        self.pos=np.array([0,0], dtype='f')
        self.z=np.double(0)  #Altura del personaje
        self.hsuelo=self.z
        self.velz=0.0
        self.angle=np.double(0) #Angulo de direccion
        self.direccion=np.array([1, 0], dtype='f')
        self.actdireccion()
        self.setpos(0,0,0)

    def setdimension(self,offset,altura):
        self.OFFSET=offset
        self.ALTURA=altura
     
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
            
    def actualiza(self,t):
        self.actualizafisica(t,9.81)
    
    def actualizafisica(self,t,g):

        #calculamos la altura del suelo
        self.hsuelo=self.mapa.floorheight(self.pos[0],self.pos[1],self.z)
        self.htecho=self.mapa.ceilheight(self.pos[0],self.pos[1],self.z)
        #print (self.hsuelo,"-",self.htecho)

        #miramos si la caida es muy grande comprobamos los cuatro puntos del suelo
        if self.hsuelo<self.z-0.5:
            self.hsuelo=max([self.mapa.floorsheight(self.pos[0],self.pos[1],self.z,self.OFFSET),
            self.mapa.wallsheight(None,self.pos[0],self.pos[1],self.z,self.OFFSET)])
            
        #miramos si tenemos que caer o subir
        if self.hsuelo<self.z or self.velz>0:
            self.z+=t*self.velz-0.5*g*t*t
            self.velz-=g*t
        if self.z+self.ALTURA>self.htecho:
            self.velz=0
            self.z=self.htecho-self.ALTURA
            
        if self.hsuelo>self.z:
            self.velz=0
            self.z=self.hsuelo

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
        h=self.mapa.wallsheight(self,pos[0],pos[1],self.z,self.OFFSET)
        if h-self.z>0.2: #Este es el salto maximo que se puede hacer
            return True
        else:
            return False
