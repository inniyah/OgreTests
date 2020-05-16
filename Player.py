#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:48:00 2020

@author: arky
"""
import numpy as np
import Ogretmxmap
import Ogre
import Liveobject



class Player(Liveobject.LiveObject):
    
    #Define velocidades del personaje
    LINEAL_VEL=5
    ANGULAR_VEL=1
    
    def __init__(self,node):
        """set node as node attached to player"""
        super(Player,self).__init__(node)
        self.keyright=False
        self.keyleft=False
        self.keyup=False
        self.keydown=False
        self.keyjump=False
        self.setpos(0,0,0)
        self.setdimension(0.25,1.5)
             
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
                self.velz=5.0
        
        self.actualizafisica(t,9.81)
    