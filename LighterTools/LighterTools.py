import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import os

class AutoAssemblyBuilder():
#UI/PIPELINE PART
    # def __init__(self, rootDir='Q:\\Info5Film\\Heritage\\04_Assembly\\'):
    def __init__(self, rootDir='Q:\\Info5Film\\Heritage\\04_Assembly\\'):
        
        self.rootDir = rootDir
        self.seqPlDirs = []
        self.seq = self.pl = None
        
        self.write_path = ''

        self.seqDirs = [x for x in os.listdir(rootDir)
                       if os.path.isdir(os.path.join(rootDir, x))]
        self.seq = self.seqDirs[0]
        
        self.buildUI()
        
        self._seqChanged(self.seq)

    
    #WINDOW
    def buildUI(self):
        self.winName2 = "LightSceneTools"
        if cmds.window(self.winName2, exists=True):
          cmds.deleteUI(self.winName2)
        #Windows Settings
        winTitle = "AutoLightSceneBuilder"
        self.winName = "AutoLightSceneBuilder"
        winWidth = 250
        if cmds.window(self.winName, exists=True):
          cmds.deleteUI(self.winName)
        cmds.window(self.winName, width=winWidth, title=winTitle)
        
        #UI code
        mainCL = cmds.columnLayout() 
        mainRLWidth = winWidth*0.99
        mainRL = cmds.rowLayout(w=winWidth, numberOfColumns=1, columnWidth1=mainRLWidth, rowAttach=((1, 'top', 0)))
        cmds.columnLayout(w=mainRLWidth) # create a columnLayout under the first row of mainRL
        
        tmpRowWidth = mainRLWidth*1
        cmds.rowLayout(numberOfColumns=1, columnWidth1=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = [mainRLWidth*0.20, mainRLWidth*0.80]
        cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
        cmds.text(label='__SEQ :', width=tmpRowWidth[0], al='right')
        cmds.optionMenu('OMSeqValue', width=tmpRowWidth[1], cc=self._seqChanged)
        for i in self.seqDirs:
            cmds.menuItem(label=i)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = [mainRLWidth*0.20, mainRLWidth*0.80]
        cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
        cmds.text(label='__PL :', width=tmpRowWidth[0], al='right')
        cmds.optionMenu('OMPlValue', width=tmpRowWidth[1], cc=self._plChanged)
        for i in self.seqPlDirs:
            cmds.menuItem(label=i)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = mainRLWidth*1
        cmds.rowLayout(numberOfColumns=1, columnWidth1=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = [mainRLWidth*0.1, mainRLWidth*0.4, mainRLWidth*0.4, mainRLWidth*0.1]
        cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth[0])
        cmds.button(label='Import', width=tmpRowWidth[1], height=30, align='center', command=self.importFiles)
        cmds.button(label='Already Import', width=tmpRowWidth[2], height=30, align='center', command=self.alredyImport)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        cmds.showWindow(self.winName)
        cmds.window(self.winName, e=True, width=winWidth, height=1)
        return
        
    #FIND SEQ DIR AND UPDATE UI
    def _seqChanged(self, newSQSelItem):
        self.seq = newSQSelItem
        
        seqDir = os.path.join(self.rootDir, self.seq)
        self.seqPlDirs = [x for x in os.listdir(seqDir)
                          if os.path.isdir(os.path.join(seqDir, x))]
        if not self.seqPlDirs:
            self.plan = None
        else:
            self.plan = self.seqPlDirs[0]
        
        for item in cmds.optionMenu('OMPlValue', q=True, ill=True) or []:
            cmds.deleteUI(item)
            
        if not self.seqPlDirs:
            cmds.menuItem(label = self.plan, parent = 'OMPlValue')
        else:
            for item in self.seqPlDirs:
                cmds.menuItem(label = item, parent = 'OMPlValue')
        
        self._plChanged(self.plan)
        
    #Find Full Directory (SEQ+PLAN)
    def _plChanged(self, newPLSelItem):
        p = newPLSelItem
        if p:
            self.pl = p
            self.plDir = os.path.join(self.rootDir, self.seq, p)
        else:
            self.pl = None
        
    #CA COMMENCE
    
    #Import des elements dans le dossier
    #1. les fichiers maya (Characters/Cars/BG(+Mash)/Lights)
    #2. les fichiers alembics d'animation
    #4. les fichiers alembics (FX?)
    #3. les VDB (fichiers FX)
    
    #Lauch Import
    def importFiles(self, clicked):
        self.importMafiles()
        self.nextStep()
        
    
    #Import Mayafiles
    def importMafiles(self):
        listMayaEXT = ['.ma', '.mb']
        listAlembicEXT = ['.abc']
        self.listImported = []
        for i in os.listdir(self.plDir):
            #print 'i=' + i
            TmpFileSplit = os.path.splitext(i)
            if TmpFileSplit[1] in listMayaEXT:
                if TmpFileSplit[1] in listMayaEXT[0]:
                    fileTyp = 'mayaAscii'
                    
                if TmpFileSplit[1] in listMayaEXT[1]:
                    fileTyp = 'mayaBinary'
                    
                NSName = TmpFileSplit[0]
                self.listImported.append(NSName)
                maFilePath = os.path.join(self.plDir, i)
                
                #import maFilePath
                #cmds.file(maFilePath, i=True, typ=fileTyp, iv=True, ra=True, mnc=False, ns=NSName, op='v=0', pr=True)
                TmpMaFileNameSplit = i.split('__')
                for o in os.listdir(self.plDir):
                    #print 'o=' +o
                    TmpFileSplit = os.path.splitext(o)
                    if TmpFileSplit[1] in listAlembicEXT:
                        TmpABCFileNameSplit = o.split('__')
                        #print "TmpABCFileNameSplit = " +str(TmpABCFileNameSplit)
                        #print "TmpMaFileNameSplit = " +TmpMaFileNameSplit[1]
                        if TmpMaFileNameSplit[1] in TmpABCFileNameSplit:
                            abcFilePath = os.path.join(self.plDir, o)
                            abcFilePath = abcFilePath.replace("\\", "/")
                            cmds.select(NSName+':GRP_Meshes_Set')
                            tmpSel = cmds.ls(sl=1)
                            tmpSelList = " ".join(tmpSel).encode('utf-8')
                            #import abcFilePath
                            command = 'AbcImport -mode import -connect "{}" "{}";'.format(tmpSelList, abcFilePath)
                            mel.eval(command) #Trouver comment avoir les nom des meshs a remplacer / Namespace?
    
    #Lauch Import
    def alredyImport(self, clicked):
        listMayaEXT = ['.ma', '.mb']
        self.listImported = []
        for i in os.listdir(self.plDir):
            TmpFileSplit = os.path.splitext(i)
            if TmpFileSplit[1] in listMayaEXT:
                if TmpFileSplit[1] in listMayaEXT[0]:
                    fileTyp = 'mayaAscii'
                    
                if TmpFileSplit[1] in listMayaEXT[1]:
                    fileTyp = 'mayaBinary'
                    
                NSName2 = TmpFileSplit[0]
                self.listImported.append(NSName2)
        self.nextStep()
    
    def nextStep(self):
        print self.listImported
        if cmds.window(self.winName, exists=True):
          cmds.deleteUI(self.winName)
        #Windows Settings
        winTitle2 = "LightSceneTool"
        self.winName2 = "LightSceneTools"
        winWidth = 250
        if cmds.window(self.winName2, exists=True):
          cmds.deleteUI(self.winName2)
        cmds.window(self.winName2, width=winWidth, title=winTitle2)
        
        #UI code
        mainCL = cmds.columnLayout() 
        mainRLWidth = winWidth*0.99
        mainRL = cmds.rowLayout(w=winWidth, numberOfColumns=1, columnWidth1=mainRLWidth, rowAttach=((1, 'top', 0)))
        cmds.columnLayout(w=mainRLWidth) # create a columnLayout under the first row of mainRL
        
        tmpRowWidth = mainRLWidth*1
        cmds.rowLayout(numberOfColumns=1, columnWidth1=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__Taylor__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('Taylor', label='Taylor :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('Taylor', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__Cobra__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('Cobra', label='Cobra :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('Cobra', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__CobraBoost__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('CobraBoost', label='CobraBoost :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('CobraBoost', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__Dragster__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('Dragster', label='Dragster :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('Dragster', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__Grace__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('Grace', label='Grace :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('Grace', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__Gurkha__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('Gurkha', label='Gurkha :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('Gurkha', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__GurkhaBoost__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('GurkhaBoost', label='GurkhaBoost :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('GurkhaBoost', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        if 'LD__MonsterTruck__' in self.listImported:
            tmpRowWidth = [mainRLWidth*0.35, mainRLWidth*0.10, mainRLWidth*0.35, mainRLWidth*0.20]
            cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
            cmds.text('MonsterTruck', label='MonsterTruck :', width=tmpRowWidth[0], al='right')
            cmds.text(label='', width=tmpRowWidth[1], al='right')
            cmds.button(label='Hide', width=tmpRowWidth[2], height=20, align='center', command=partial(self.hideSmthing, cmds.text('MonsterTruck', q=1, label=True)))
            cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = mainRLWidth*1
        cmds.rowLayout(numberOfColumns=1, columnWidth1=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        tmpRowWidth = [mainRLWidth*0.25, mainRLWidth*0.5, mainRLWidth*0.25]
        cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth[0])
        cmds.button(label='Delete all except lights', width=tmpRowWidth[1], height=30, align='center', command=self.deleteAllNoLight)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        cmds.showWindow(self.winName2)
        cmds.window(self.winName2, e=True, width=winWidth, height=1)
        return
        
    def hideSmthing(self, smthing, *args):
        if smthing == 'Taylor :':
            try:
                tmpGrpToExport = "LD__Taylor__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
                
                    
            except Exception as ex:
                print 'No Taylor'
                
        if smthing == 'Cobra :':
            try:
                tmpGrpToExport = "LD__Cobra__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No Cobra'
                
        if smthing == 'CobraBoost :':
            try:
                tmpGrpToExport = "LD__CobraBoost__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No CobraBoost'
                
        if smthing == 'Dragster :':
            try:
                tmpGrpToExport = "LD__Dragster__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No Dragter'
                
        if smthing == 'Grace :':
            try:
                tmpGrpToExport = "LD__Grace__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No Grace'
                
        if smthing == 'Gurkha :':
            try:
                tmpGrpToExport = "LD__Gurkha__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No Gurkha'
                
        if smthing == 'GurkhaBoost :':
            try:
                tmpGrpToExport = "LD__GurkhaBoost__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No GurkhaBoost'
                
        if smthing == 'MonsterTruck :':
            try:
                tmpGrpToExport = "LD__MonsterTruck__:" + 'GRP_Meshes_Set' 
                cmds.select(tmpGrpToExport)
                tmpsel = cmds.ls(sl=1)
                testvis = cmds.getAttr(tmpsel[0]+'.visibility')
                if testvis:
                    cmds.hide(tmpsel, cs=1)
                else:
                    cmds.showHidden(tmpsel)
            except Exception as ex:
                print 'No MonsterTruck'
                
    def deleteAllNoLight(self, *arg):
        print 'BOOOOM'
        lights = []
        lightLists = mc.ls(type="lightList")
        for lightList in lightLists:
            lights += mc.listConnections("{0}.lights".format(lightList))
            print lights
        cmds.select(lights)
        lightsParents = cmds.listRelatives(lights, s=True)
        cmds.select(lightsParents, add=True)
        toNotDelete = cmds.ls(sl=1)
        cmds.select(all=True)
        cmds.select(toNotDelete, d=True)
        toDelete = cmds.ls(sl=1)
        cmds.delete(toDelete)
        
p = AutoAssemblyBuilder()