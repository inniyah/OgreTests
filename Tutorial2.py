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
        
        # -- tutorial section start --
        # Creamos la camara y la posicionamos en la escena
        camNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        cam = scn_mgr.createCamera("myCam")
        camNode.setPosition(200, 300, 400)
        camNode.lookAt(Ogre.Vector3(0, 0, 0), Ogre.Node.TS_WORLD)
        cam.setNearClipDistance(5)
        camNode.attachObject(cam)
        vp = self.getRenderWindow().addViewport(cam);
        vp.setBackgroundColour(Ogre.ColourValue(0, 0, 0));
        #cam.setAspectRatio(Ogre.Real(vp.getActualWidth()) / Ogre.Real(vp.getActualHeight()))
        cam.setAspectRatio((vp.getActualWidth()) / (vp.getActualHeight()))
    
        #Put entities
        ninjaEntity = scn_mgr.createEntity("ninja.mesh")
        ninjaEntity.setCastShadows(True)
        scn_mgr.getRootSceneNode().createChildSceneNode().attachObject(ninjaEntity)

        #make a plane
        plane=Ogre.Ogre.Plane()
        n=plane.normal
        n.x,n.y,n.z=0,1,0
        #plane.d=5000
        #plane=Ogre.Ogre.Plane(Ogre.Vector3(0,1,0))
        #Plane plane(Vector3::UNIT_Y, 0);
        Ogre.MeshManager.getSingleton().createPlane(
            "ground", Ogre.Ogre.RGN_DEFAULT,
            plane,
            1500, 1500, 20, 20,
            True,
            1, 5, 5,
            Ogre.Vector3(0,0,1))

        groundEntity = scn_mgr.createEntity("ground")
        scn_mgr.getRootSceneNode().createChildSceneNode().attachObject(groundEntity)
        groundEntity.setCastShadows(False)
        groundEntity.setMaterialName("Examples/Rockwall")

        scn_mgr.setAmbientLight(Ogre.ColourValue(0, 0, 0))
        scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_STENCIL_MODULATIVE)

        spotLight = scn_mgr.createLight("SpotLight")

        spotLight.setDiffuseColour(0, 0, 1.0)
        spotLight.setSpecularColour(0, 0, 1.0)
        spotLight.setType(Ogre.Ogre.Light.LT_SPOTLIGHT);

        spotLightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        spotLightNode.attachObject(spotLight)
        spotLightNode.setDirection(-1, -1, 0)
        spotLightNode.setPosition(Ogre.Vector3(200, 200, 0))
        #spotLight.setSpotlightRange(Ogre.Degree(35), Ogre.Degree(50));
        spotLight.setSpotlightRange(Ogre.Radian(0.61), Ogre.Radian(0.8727))
        
        directionalLight = scn_mgr.createLight("DirectionalLight")
        directionalLight.setType(Ogre.Light.LT_DIRECTIONAL);
        directionalLight.setDiffuseColour(Ogre.ColourValue(0.4, 0, 0));
        directionalLight.setSpecularColour(Ogre.ColourValue(0.4, 0, 0))
        directionalLightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        directionalLightNode.attachObject(directionalLight)
        directionalLightNode.setDirection(Ogre.Vector3(0, -1, 1))

        pointLight = scn_mgr.createLight("PointLight")
        pointLight.setType(Ogre.Light.LT_POINT)

        pointLight.setDiffuseColour(0.3, 0.3, 0.3)
        pointLight.setSpecularColour(0.3, 0.3, 0.3)
        pointLightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
        pointLightNode.attachObject(pointLight)
        pointLightNode.setPosition(Ogre.Vector3(0, 150, 250))
    
    def keyPressed(self, evt):
            if evt.keysym.sym == OgreBites.SDLK_ESCAPE:
                self.getRoot().queueEndRendering()
    
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

