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
import Player


def gettilepos(vector):
    return [vector.x,vector.z]
    

RGN_MESHVIEWER = "OgreMeshViewer"


class Tutorial6(OgreBites.ApplicationContext, OgreBites.InputListener):
    def __init__(self):
        OgreBites.ApplicationContext.__init__(self, "Titulo de la ventana")
        OgreBites.InputListener.__init__(self)
        #self.pos=Ogre.Vector3(-1,1.5,0) #altura 1.80m
        self.LINEAL_VEL=5
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
        scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_TEXTURE_MODULATIVE)
        #scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_STENCIL_MODULATIVE)
 
        #Creamos el mapa
        mapa=Ogretmxmap.tmxmap("Maps/map.tmx")
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.setPosition(0,0,0)
        mapa.createmap(scn_mgr)

       
        # Vamos a crear el nodo perteneciente al personaje
        Playernode=scn_mgr.getRootSceneNode().createChildSceneNode()
        #Playernode.setPosition(self.pos)        
        self.Playernode=Playernode
        # Creo el player y lo fusiono con su nodo
        self.Player=Player.Player(Playernode)
        self.Player.mapa=mapa
        self.Player.setpos(0,0,0)

        
        # Creamos la camara y la posicionamos en el personaje
        camNode = Playernode.createChildSceneNode()
        camNode.setPosition(0,1.5,0)
        cam = scn_mgr.createCamera("MainCam")
        #camNode.setPosition(0, 0, 80)
        camNode.lookAt(Ogre.Vector3(300, 1.5, 0), Ogre.Node.TS_WORLD)
        cam.setNearClipDistance(.2)
        camNode.attachObject(cam)
        vp = self.getRenderWindow().addViewport(cam)
        vp.setBackgroundColour(Ogre.ColourValue(0, 0, 0))
        cam.setAspectRatio((vp.getActualWidth()) / (vp.getActualHeight()))

        self.camNode=camNode

        # Setup the scene

        scn_mgr.setAmbientLight(Ogre.ColourValue(.5, .5, .5))
        light=scn_mgr.createLight("MainLight")
        light.setType(Ogre.Light.LT_DIRECTIONAL);
        light.setDiffuseColour(Ogre.ColourValue(.7, .0, .0));
        light.setSpecularColour(Ogre.ColourValue(.3, .3, 0))
        light.setDirection(1, -1, 0)
        
#        lightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
#        lightNode.attachObject(light)
#        lightNode.setPosition(0, 3, 0)

        pointLight = scn_mgr.createLight("PointLight")
        pointLight.setType(Ogre.Light.LT_POINT)

        pointLight.setDiffuseColour(0.3, 0.3, 0.3)
        pointLight.setSpecularColour(0.3, 0.3, 0.3)
        pointLightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        pointLightNode.attachObject(pointLight)
        #pointLightNode.setPosition(Ogre.Vector3(2, 2, 2))
        pointLightNode.setPosition(2, 2, 2)

        
        #manual object (y,z,x)

        #mapa.load("Maps/mapa.tmx")
        #floor1=mapa.makefloor(scn_mgr,"Floor1",0)
        #ceil1=mapa.makeceil(scn_mgr,"Ceil1",2)
        #mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        #mannode.setPosition(0,0,0)
        #mannode.attachObject(floor1)
        #mannode.attachObject(ceil1)
        #mapa.makewalls(scn_mgr,"Wall1",0)
        self.mapa=mapa
        
        
        #lets set a fog
        Fadecolor=Ogre.ColourValue(0,0,0)
        vp.setBackgroundColour(Fadecolor)
        scn_mgr.setFog(Ogre.Ogre.FOG_LINEAR,Fadecolor,0,600,900)
        

    def frameStarted(self, evt):
        OgreBites.ApplicationContext.frameStarted(self, evt)
        
        
        self.time=evt.timeSinceLastFrame
        self.Player.actualizanodo()
        #self.vel=self.time*self.LINEAL_VEL
        #print (evt.timeSinceLastFrame)
                        
        return True
        
    
    def keyPressed(self, evt):
            if evt.keysym.sym == OgreBites.SDLK_ESCAPE:
                self.getRoot().queueEndRendering()
            
            if evt.keysym.sym == OgreBites.SDLK_DOWN:
                self.Player.backward(self.time)

                
            if evt.keysym.sym == OgreBites.SDLK_UP:
                self.Player.fordward(self.time)
  
            
            if evt.keysym.sym == OgreBites.SDLK_LEFT:
                self.Player.rotateleft(self.time)

            
            if evt.keysym.sym == OgreBites.SDLK_RIGHT:
                self.Player.rotateright(self.time)
 
            
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

