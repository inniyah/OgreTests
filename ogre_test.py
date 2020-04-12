#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import Ogre
import Ogre.RTShader as OgreRTShader
import Ogre.Bites as OgreBites

from Ogre.Overlay import *

class MaterialCreator(Ogre.MeshSerializerListener):
    def __init__(self):
        Ogre.MeshSerializerListener.__init__(self)

    def processMaterialName(self, mesh, name):
        # ensure some material exists so we can display the name
        mat_mgr = Ogre.MaterialManager.getSingleton()
        if not mat_mgr.resourceExists(name, mesh.getGroup()):
            try:
                mat_mgr.create(name, mesh.getGroup())
            except RuntimeError:
                # do not crash if name is ""
                # this is illegal due to OGRE specs, but we want to show that in the UI
                pass

    def processSkeletonName(self, mesh, name): pass
    def processMeshCompleted(self, mesh): pass

class MainOgreApp(OgreBites.ApplicationContext, OgreBites.InputListener):

    RGN_THIS_APP = "OgreTest"

    def __init__(self, args, resources_cfg):
        OgreBites.ApplicationContext.__init__(self, "Ogre Test")
        OgreBites.InputListener.__init__(self)
        self.rescfg = resources_cfg
        self.restart = False

    def keyPressed(self, evt):
        if evt.keysym.sym == OgreBites.SDLK_ESCAPE:
            self.getRoot().queueEndRendering()
        return True

    def mousePressed(self, evt):
        return True

    def _save_screenshot(self):
        name = os.path.splitext(self.meshname)[0]
        outpath = os.path.join(self.meshdir, "screenshot_{}_".format(name))

        self.cam.getViewport().setOverlaysEnabled(False)
        self.getRoot().renderOneFrame()
        self.getRenderWindow().writeContentsToTimestampedFile(outpath, ".png")
        self.cam.getViewport().setOverlaysEnabled(True)

    def frameStarted(self, evt):
        OgreBites.ApplicationContext.frameStarted(self, evt)

        if not self.cam.getViewport().getOverlaysEnabled():
            return True

        ImGuiOverlay.NewFrame(evt)

        if BeginMainMenuBar():
            if BeginMenu("File"):
                if MenuItem("Select Renderer"):
                    self.getRoot().queueEndRendering()
                    self.restart = True
                if MenuItem("Save Screenshot", "P"):
                    self._save_screenshot()
                if MenuItem("Quit", "Esc"):
                    self.getRoot().queueEndRendering()
                EndMenu()
            EndMainMenuBar()

        return True

    def locateResources(self):
        rgm = Ogre.ResourceGroupManager.getSingleton()
        # ensure our resource group is separate, even with a local resources.cfg
        rgm.createResourceGroup(self.RGN_THIS_APP, False)

        # use parent implementation to locate system-wide RTShaderLib
        OgreBites.ApplicationContext.locateResources(self)

        if self.rescfg:
            cfg = Ogre.ConfigFile()
            cfg.loadDirect(self.rescfg)

            for sec, settings in cfg.getSettingsBySection().items():
                for kind, loc in settings.items():
                    rgm.addResourceLocation(loc, kind, sec)

        if not rgm.resourceLocationExists('.', Ogre.RGN_DEFAULT):
            rgm.addResourceLocation('.', "FileSystem", Ogre.RGN_DEFAULT)

    def setup(self):
        OgreBites.ApplicationContext.setup(self)
        self.addInputListener(self)

        self.restart = False
        imgui_overlay = ImGuiOverlay()
        GetIO().IniFilename = self.getFSLayer().getWritablePath("imgui.ini")

        root = self.getRoot()
        scn_mgr = root.createSceneManager()
        scn_mgr.addRenderQueueListener(self.getOverlaySystem())
        self.scn_mgr = scn_mgr

        # set listener to deal with missing materials
        self.mat_creator = MaterialCreator()
        Ogre.MeshManager.getSingleton().setListener(self.mat_creator)

        # for picking
        self.ray_query = scn_mgr.createRayQuery(Ogre.Ray())

        #imgui_overlay.addFont("SdkTrays/Value", self.RGN_THIS_APP)
        imgui_overlay.show()
        OverlayManager.getSingleton().addOverlay(imgui_overlay)
        imgui_overlay.disown() # owned by OverlayMgr now

        shadergen = OgreRTShader.ShaderGenerator.getSingleton()
        shadergen.addSceneManager(scn_mgr)  # must be done before we do anything with the scene

        scn_mgr.setAmbientLight(Ogre.ColourValue(.1, .1, .1))

        self.highlight_mat = Ogre.MaterialManager.getSingleton().create("Highlight", self.RGN_THIS_APP)
        self.highlight_mat.getTechniques()[0].getPasses()[0].setEmissive(Ogre.ColourValue(1, 1, 0))

        unit = 1.

        axes_node = scn_mgr.getRootSceneNode().createChildSceneNode()
        axes_node.getDebugRenderable()  # make sure Ogre/Debug/AxesMesh is created
        self.axes = scn_mgr.createEntity("Ogre/Debug/AxesMesh")
        axes_node.attachObject(self.axes)
        axes_node.setScale(Ogre.Vector3(unit))
        self.axes.setVisible(True)
        self.axes.setQueryFlags(0) # exclude from picking

        self.cam = scn_mgr.createCamera("myCam")
        self.cam.setNearClipDistance(unit * 0.01)
        self.cam.setAutoAspectRatio(True)
        camnode = scn_mgr.getRootSceneNode().createChildSceneNode()
        camnode.attachObject(self.cam)

        light = scn_mgr.createLight("MainLight")
        light.setType(Ogre.Light.LT_DIRECTIONAL)
        light.setSpecularColour(Ogre.ColourValue.White)
        camnode.attachObject(light)

        vp = self.getRenderWindow().addViewport(self.cam)
        vp.setBackgroundColour(Ogre.ColourValue(.3, .3, .3))

        self.camman = OgreBites.CameraMan(camnode)
        self.camman.setStyle(OgreBites.CS_ORBIT)
        self.camman.setYawPitchDist(Ogre.Radian(0), Ogre.Radian(0.3), 10)
        self.camman.setFixedYaw(False)

        self.imgui_input = OgreBites.ImGuiInputListener()
        self.input_dispatcher = OgreBites.InputListenerChain([self.imgui_input, self.camman])
        self.addInputListener(self.input_dispatcher)

    def shutdown(self):
        OgreBites.ApplicationContext.shutdown(self)

        if self.restart:
            self.getRoot().shutdown()
            self.getRoot().setRenderSystem(None) # make sure empty rendersystem is written




if __name__ == "__main__":
    import argparse

    resources_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources.cfg")

    parser = argparse.ArgumentParser(description="Ogre Test")
    args = parser.parse_args() 
    app = MainOgreApp(args, resources_cfg)

    while True: # allow auto restart
        app.initApp()
        app.getRoot().startRendering()
        app.closeApp()

        if not app.restart: break
