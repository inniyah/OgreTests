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
import ctypes as ctypes

import Ogre.Terrain as ogreterrain

from Ogre.Overlay import *

RGN_MESHVIEWER = "OgreMeshViewer"
TERRAIN_PAGE_MIN_X = 0
TERRAIN_PAGE_MIN_Y = 0
TERRAIN_PAGE_MAX_X = 0
TERRAIN_PAGE_MAX_Y = 0

def Clamp ( val, low, high ):
    if val < low: return low
    if val > high: return high
    return val

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
     
    def defineTerrain(self, x, y):
        print("define terrain (%i,%i)"%(x,y))
        filename = self.mTerrainGroup.generateFilename(x, y)
        RGM = Ogre.ResourceGroupManager.getSingleton()
        #self.mTerrainsImported = False
        if ( RGM.resourceExists(self.mTerrainGroup.getResourceGroup(), filename) ):
            self.mTerrainGroup.defineTerrain(x, y)
        else :
            img = self.getTerrainImage((x % 2) != 0, (y%2) != 0)
            self.mTerrainGroup.defineTerrain(x, y, img)
            self.mTerrainsImported = True
   
    def getTerrainImage(self, flipX, flipY):
        img = Ogre.Image()
        img.load("terrain.png", Ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
        if flipX:
            img.flipAroundY()
        if flipY:
            img.flipAroundX()
        return img
    
    def configureTerrainDefaults(self, light):
        self.mTerrainGlobals.setMaxPixelError(8)
        self.mTerrainGlobals.setCompositeMapDistance(3000)
        self.mTerrainGlobals.setLightMapDirection(light.getDerivedDirection())
        self.mTerrainGlobals.setCompositeMapAmbient(self.scn_mgr.getAmbientLight())
        self.mTerrainGlobals.setCompositeMapDiffuse(light.getDiffuseColour())

        #// Configure default import settings for if we use imported image
        #defaultimp = self.mTerrainGroup.getDefaultImportSettings()
        defaultimp = self.mTerrainGroup
        defaultimp.terrainSize = 513
        defaultimp.worldSize = 12000
        defaultimp.inputScale = 600
        defaultimp.minBatchSize = 33
        defaultimp.maxBatchSize = 65

        # textures
#        defaultimp.layerList.resize(3)
#        defaultimp.layerList[0].worldSize = 100
#        defaultimp.layerList[0].textureNames.push_back("grass_green-01_diffusespecular.dds")
#        defaultimp.layerList[0].textureNames.push_back("grass_green-01_normalheight.dds")
#        defaultimp.layerList[1].worldSize = 100
#        defaultimp.layerList[1].textureNames.push_back("dirt_grayrocky_diffusespecular.dds")
#        defaultimp.layerList[1].textureNames.push_back("dirt_grayrocky_normalheight.dds")
#        defaultimp.layerList[2].worldSize = 200
#        defaultimp.layerList[2].textureNames.push_back("growth_weirdfungus-03_diffusespecular.dds")
#        defaultimp.layerList[2].textureNames.push_back("growth_weirdfungus-03_normalheight.dds")
#        defaultimp.layerList.append(ogreterrain.Terrain.LayerInstance() )
#        defaultimp.layerList.append(ogreterrain.Terrain.LayerInstance() )
#        defaultimp.layerList.append(ogreterrain.Terrain.LayerInstance() )
#
#        defaultimp.layerList[0].worldSize = 100
#        defaultimp.layerList[0].textureNames.append("dirt_grayrocky_diffusespecular.dds")
#        defaultimp.layerList[0].textureNames.append("dirt_grayrocky_normalheight.dds")
#        defaultimp.layerList[1].worldSize = 30
#        defaultimp.layerList[1].textureNames.append("grass_green-01_diffusespecular.dds")
#        defaultimp.layerList[1].textureNames.append("grass_green-01_normalheight.dds")
#        defaultimp.layerList[2].worldSize = 200
#        defaultimp.layerList[2].textureNames.append("growth_weirdfungus-03_diffusespecular.dds")
#        defaultimp.layerList[2].textureNames.append("growth_weirdfungus-03_normalheight.dds")

    def initBlendMaps(self, terrain):
        blendMap0 = terrain.getLayerBlendMap(1)
        blendMap1 = terrain.getLayerBlendMap(2)
        minHeight0 = 70
        fadeDist0 = 40.0
        minHeight1 = 70
        fadeDist1 = 15.0
    
        pBlend1 = blendMap1.getBlendPointer() # returns the address of the buffer
        size = terrain.getLayerBlendMapSize() * terrain.getLayerBlendMapSize()
        blend_data=(ctypes.c_float * size).from_address(pBlend1)
        index = 0
        for y in range(terrain.getLayerBlendMapSize()):
            for x in range( terrain.getLayerBlendMapSize() ):
                # using ctypes
                tx=ctypes.c_float(0.0)
                ty=ctypes.c_float(0.0)
    
        blendMap0.convertImageToTerrainSpace(x, y, ctypes.addressof(tx), ctypes.addressof(ty))
        height = terrain.getHeightAtTerrainPosition(tx.value, ty.value)
        val = (height - minHeight0) / fadeDist0
        val = Clamp(val, 0, 1)
        
        val = (height - minHeight1) / fadeDist1
        val = Clamp(val, 0, 1)
        blend_data [index] = val
        index += 1
        
        blendMap0.dirty()
        blendMap1.dirty()
        blendMap0.update()
        blendMap1.update()


        
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
        mTerrainPos=Ogre.Vector3(1000,0,5000)
        
        camNode.setPosition(mTerrainPos + Ogre.Vector3(1683, 50, 2116))
        camNode.lookAt(Ogre.Vector3(1963, 50, 1660), Ogre.Node.TS_PARENT)
        cam.setNearClipDistance(40) # tight near plane important for shadows

        if root.getRenderSystem().getCapabilities().hasCapability(Ogre.RSC_INFINITE_FAR_PLANE):
            print ("ponemos far clip distance a infinito")
            cam.setFarClipDistance(0)# enable infinite far clip distance if we can
        else:
            cam.setFarClipDistance(50000)
    
        camNode.attachObject(cam)
        vp = self.getRenderWindow().addViewport(cam);
        vp.setBackgroundColour(Ogre.ColourValue(0, 0, 0));
        
        #Ponemos las luces
        l = scn_mgr.createLight("tstLight")
        l.setType(Ogre.Light.LT_DIRECTIONAL)
        l.setDiffuseColour(Ogre.ColourValue.White)
        l.setSpecularColour(Ogre.ColourValue(0.4, 0.4, 0.4))
        ln = scn_mgr.getRootSceneNode().createChildSceneNode()
        ln.setDirection(Ogre.Vector3(0.55, -0.3, 0.75).normalisedCopy())
        ln.attachObject(l)
        
        #Terreno
        TERRAIN_SIZE=513
        TERRAIN_WORLD_SIZE=12000
        #scn_mgr.setWorldGeometry("terrain.cfg")
        self.mTerrainGlobals = ogreterrain.TerrainGlobalOptions()
        mTerrainGroup = ogreterrain.TerrainGroup(scn_mgr, ogreterrain.Terrain.ALIGN_X_Z, TERRAIN_SIZE, TERRAIN_WORLD_SIZE)
        self.mTerrainGroup=mTerrainGroup
        mTerrainGroup.setFilenameConvention("BasicTutorial3Terrain", "dat")
        mTerrainGroup.setOrigin(mTerrainPos)
        
        self.configureTerrainDefaults(l)
        
        self.defineTerrain(0, 0)
        for x in range(TERRAIN_PAGE_MIN_X,TERRAIN_PAGE_MAX_X):
            for y in range(TERRAIN_PAGE_MIN_Y,TERRAIN_PAGE_MAX_Y):
                self.defineTerrain(x, y)
                
        # sync load since we want everything in place when we start
        mTerrainGroup.loadAllTerrains(True)
        
        if (self.mTerrainsImported):   
            for t in mTerrainGroup.getTerrainIterator():
                self.initBlendMaps(t.instance())
        
        mTerrainGroup.freeTemporaryResources()
        #self.terrainGlobals = ogreterrain.TerrainGlobalOptions()
        #self.configureTerrainDefaults(l)
    
    
    
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

