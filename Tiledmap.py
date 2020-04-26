#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:05:57 2020

@author: arky
"""
import Ogre
import Ogre.RTShader as OgreRTShader
import Ogre.Bites as OgreBites
import os.path
import Ogretmxmap

from Ogre.Overlay import *

RGN_MESHVIEWER = "OgreMeshViewer"


class Tutorial6(OgreBites.ApplicationContext, OgreBites.InputListener):
    def __init__(self):
        OgreBites.ApplicationContext.__init__(self, "Titulo de la ventana")
        OgreBites.InputListener.__init__(self)
        self.pos=Ogre.Vector3(0,18,80) #altura 1.80m
        self.LINEAL_VEL=50
        self.ANGULAR_VEL=1
        
    def frameStarted(self, evt):
        return True
#        OgreBites.ApplicationContext.frameStarted(self, evt)
#        
#        if not self.cam.getViewport().getOverlaysEnabled():
#            return True
#
#        ImGuiOverlay.NewFrame(evt)
        
    def locateResources(self):
        
        self.rescfg= os.path.basename("./resources.cfg")
        self.meshdir = os.path.dirname("./resources.cfg")
        
        rgm = Ogre.ResourceGroupManager.getSingleton()
        # ensure our resource group is separate, even with a local resources.cfg
        rgm.createResourceGroup(RGN_MESHVIEWER, False)

        # use parent implementation to locate system-wide RTShaderLib
        OgreBites.ApplicationContext.locateResources(self)

        # allow override by local resources.cfg
        if not self.getFSLayer().fileExists(self.rescfg):
            # we use the fonts from SdkTrays.zip
            trays_loc = self.getDefaultMediaDir()+"/packs/SdkTrays.zip"
            rgm.addResourceLocation(trays_loc, "Zip", RGN_MESHVIEWER)

        if self.rescfg:
            cfg = Ogre.ConfigFile()
            cfg.loadDirect(self.rescfg)

            for sec, settings in cfg.getSettingsBySection().items():
                for kind, loc in settings.items():
                    rgm.addResourceLocation(loc, kind, sec)

        # explicitly add mesh location to be safe
        if not rgm.resourceLocationExists(self.meshdir, Ogre.RGN_DEFAULT):
            rgm.addResourceLocation(self.meshdir, "FileSystem", Ogre.RGN_DEFAULT)
        
        
    def setup(self):
        # SETUP es la primera función a la que se llama
        # Primero llamamos a la base y ponemos el listener
        OgreBites.ApplicationContext.setup(self)
        #Ahora se llama a locate resources
        self.addInputListener(self)
               
        self.restart =False
        
        #Inicializamos ogre u hacemos un puntero a Root
        root = self.getRoot()
        
        #Creamos el scene manager
        scn_mgr = root.createSceneManager()
        scn_mgr.addRenderQueueListener(self.getOverlaySystem())
        self.scn_mgr = scn_mgr
        
        
        # Creamos el Shader
        shadergen = OgreRTShader.ShaderGenerator.getSingleton()
        shadergen.addSceneManager(scn_mgr)
        
        # Vamos a crear el nodo perteneciente al personaje
        Playernode=scn_mgr.getRootSceneNode().createChildSceneNode()
        Playernode.setPosition(self.pos)        
        self.Playernode=Playernode
        
        # Creamos la camara y la posicionamos en la escena
        camNode = Playernode.createChildSceneNode()
        cam = scn_mgr.createCamera("MainCam")
        #camNode.setPosition(0, 0, 80)
        camNode.lookAt(Ogre.Vector3(0, 0, -300), Ogre.Node.TS_WORLD)
        cam.setNearClipDistance(2)
        camNode.attachObject(cam)
        vp = self.getRenderWindow().addViewport(cam)
        vp.setBackgroundColour(Ogre.ColourValue(0, 0, 0))
        cam.setAspectRatio((vp.getActualWidth()) / (vp.getActualHeight()))

        self.camNode=camNode

        # Setup the scene
#        wall = scn_mgr.createEntity("simplewall.mesh")
#        wallNode = scn_mgr.getRootSceneNode().createChildSceneNode()
#        wallNode.attachObject(wall)

        scn_mgr.setAmbientLight(Ogre.ColourValue(.5, .5, .5))
        light=scn_mgr.createLight("MainLight")
        lightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        lightNode.attachObject(light)
        lightNode.setPosition(20, 80, 50)
        
        #manual object (y,z,x)
        mapa=Ogretmxmap.tmxmap()
        mapa.load("Maps/mapa.tmx")
        floor1=mapa.makefloor(scn_mgr,"Floor1",0)
        ceil1=mapa.makeceil(scn_mgr,"Ceil1",20)
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.setPosition(0,0,0)
        mannode.attachObject(floor1)
        mannode.attachObject(ceil1)
        mapa.makewalls(scn_mgr,"Wall1",0)
        
        
        #lets set a fog
        Fadecolor=Ogre.ColourValue(0,0,0)
        vp.setBackgroundColour(Fadecolor)
        scn_mgr.setFog(Ogre.Ogre.FOG_LINEAR,Fadecolor,0,600,900)
        

    def frameStarted(self, evt):
        OgreBites.ApplicationContext.frameStarted(self, evt)
        #if not self.cam.getViewport().getOverlaysEnabled():
        #    return True
        #ImGuiOverlay.NewFrame(evt)
        #self.camNode.setPosition(self.pos)
        self.time=evt.timeSinceLastFrame
        self.vel=self.time*self.LINEAL_VEL
        #print (evt.timeSinceLastFrame)
                        
        return True
        
    
    def keyPressed(self, evt):
            if evt.keysym.sym == OgreBites.SDLK_ESCAPE:
                self.getRoot().queueEndRendering()
            
            if evt.keysym.sym == OgreBites.SDLK_DOWN:
                self.Playernode.translate(0,0,self.time*self.LINEAL_VEL,Ogre.Ogre.Node.TS_LOCAL)
                #self.pos=self.pos+Ogre.Vector3(0,0,1)*2
                
            if evt.keysym.sym == OgreBites.SDLK_UP:
                self.Playernode.translate(0,0,-self.time*self.LINEAL_VEL,Ogre.Ogre.Node.TS_LOCAL)
                #self.pos=self.pos+Ogre.Vector3(0,0,-1)*2
            
            if evt.keysym.sym == OgreBites.SDLK_LEFT:
                self.Playernode.yaw(Ogre.Ogre.Radian(self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)
                #self.pos=self.pos+Ogre.Vector3(-1,0,0)*2
            
            if evt.keysym.sym == OgreBites.SDLK_RIGHT:
                self.Playernode.yaw(Ogre.Ogre.Radian(-self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)
                #self.pos=self.pos+Ogre.Vector3(1,0,0)*2
            
            if evt.keysym.sym == OgreBites.SDLK_PAGEDOWN:
                self.camNode.pitch(Ogre.Ogre.Radian(-self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)

            if evt.keysym.sym == OgreBites.SDLK_PAGEUP:
                self.camNode.pitch(Ogre.Ogre.Radian(self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)

            
            return True
                
    def mousePressed(self, evt):
        return True
    
    def shutdown(self):
        OgreBites.ApplicationContext.shutdown(self)
        
        if self.restart:
            # make sure empty rendersystem is written
            self.getRoot().shutdown()
            self.getRoot().setRenderSystem(None)



if __name__ == "__main__":

    app = Tutorial6()

    while True: # allow auto restart
        app.initApp()
        app.getRoot().startRendering()
        app.closeApp()

        if not app.restart: break

