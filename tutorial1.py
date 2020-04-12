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

from Ogre.Overlay import *

RGN_MESHVIEWER = "OgreMeshViewer"


class Tutorial1(OgreBites.ApplicationContext, OgreBites.InputListener):
    def __init__(self):
        OgreBites.ApplicationContext.__init__(self, "Titulo de la ventana")
        OgreBites.InputListener.__init__(self)
        
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
        self.meshdir=os.path.dirname("./resources.cfg")
        
        rgm = Ogre.ResourceGroupManager.getSingleton()
        # ensure our resource group is separate, even with a local resources.cfg
        rgm.createResourceGroup(RGN_MESHVIEWER, False)

        # use parent implementation to locate system-wide RTShaderLib
        OgreBites.ApplicationContext.locateResources(self)

        # allow override by local resources.cfg
        if not self.getFSLayer().fileExists("resources.cfg"):
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
        print("setup")
        #Primero llamamos a la base y ponemos el listener
        OgreBites.ApplicationContext.setup(self)
        self.addInputListener(self)
        
        mesh = Ogre.MeshManager.getSingleton().getByName("ogrehead.mesh")
        
        self.restart =False
        
        #get a pointer to the already created root
        #create the scene manager
        root = self.getRoot()
        scn_mgr = root.createSceneManager()
        scn_mgr.addRenderQueueListener(self.getOverlaySystem())
        self.scn_mgr = scn_mgr
        
        # must be done before we do anything with the scene
        shadergen = OgreRTShader.ShaderGenerator.getSingleton()
        shadergen.addSceneManager(scn_mgr)
        
        # Ponemos las luces
        scn_mgr.setAmbientLight(Ogre.ColourValue(0.5,0.5,0.5))
        light=scn_mgr.createLight("MainLight")
        lightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        lightNode.attachObject(light)
        lightNode.setPosition(20, 80, 50)
        
        #Ponemos la camara
        camNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        cam =scn_mgr.createCamera("myCam")
        cam.setNearClipDistance(5) # specific to this sample
        cam.setAutoAspectRatio(True)
        camNode.attachObject(cam)
        camNode.setPosition(0, 0, 140)
        
        #and tell it to render into the main window
        self.getRenderWindow().addViewport(cam)
        
        #ponemos la entidad 1
        ogreEntity = scn_mgr.createEntity("ogrehead.mesh")
        ogreNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        ogreNode.attachObject(ogreEntity);
        
        #CAmera movement
        camNode.setPosition(0, 47, 222);
    
        #Second entity
        ogreEntity2 = scn_mgr.createEntity("ogrehead.mesh")
        ogreNode2 = scn_mgr.getRootSceneNode().createChildSceneNode(Ogre.Vector3(84, 48, 0))
        ogreNode2.attachObject(ogreEntity2)

        #Third entity
        ogreEntity3 = scn_mgr.createEntity("ogrehead.mesh")
        ogreNode3 = scn_mgr.getRootSceneNode().createChildSceneNode()
        ogreNode3.setPosition(0, 104, 0)
        ogreNode3.setScale(2, 1.2, 1)
        ogreNode3.attachObject(ogreEntity3)

        #Fourth entity
        ogreEntity4 = scn_mgr.createEntity("ogrehead.mesh")
        ogreNode4 = scn_mgr.getRootSceneNode().createChildSceneNode()
        ogreNode4.setPosition(-84, 48, 0)
        #ogreNode4.roll(Ogre.Degree(-90))
        ogreNode4.roll(Ogre.Radian(-1.5508))
        ogreNode4.attachObject(ogreEntity4)

    
    def shutdown(self):
        OgreBites.ApplicationContext.shutdown(self)
        
        if self.restart:
            # make sure empty rendersystem is written
            self.getRoot().shutdown()
            self.getRoot().setRenderSystem(None)
    



if __name__ == "__main__":

    app = Tutorial1()

    while True: # allow auto restart
        app.initApp()
        app.getRoot().startRendering()
        app.closeApp()

        if not app.restart: break