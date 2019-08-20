import maya.cmds as cmds
import maya.mel as mel
import os

class AutoAssemblyBuilder():
#UI/PIPELINE PART
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
        #Windows Settings
        winTitle = "AutoAssembly"
        winName = "AutoAssembly"
        winWidth = 250
        if cmds.window(winName, exists=True):
          cmds.deleteUI(winName)
        cmds.window(winName, width=winWidth, title=winTitle)
        
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
        
        tmpRowWidth = [mainRLWidth*0.25, mainRLWidth*0.5, mainRLWidth*0.25]
        cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
        cmds.text(label='', width=tmpRowWidth[0])
        cmds.button(label='Next Step', width=tmpRowWidth[1], height=30, align='center', command=self.ImportFiles)
        cmds.setParent('..') # also can use cmds.setParent(mainRL)
        
        cmds.showWindow(winName)
        cmds.window(winName, e=True, width=winWidth, height=1)
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
    def ImportFiles(self, clicked):
        self.ImportMafiles()
        #self.ImportABCfiles()
        
    
    #Import Mayafiles
    def ImportMafiles(self):
        listMayaEXT = ['.ma', '.mb']
        listAlembicEXT = ['.abc']
        for i in os.listdir(self.plDir):
            #print 'i=' + i
            TmpFileSplit = os.path.splitext(i)
            if TmpFileSplit[1] in listMayaEXT:
                if TmpFileSplit[1] in listMayaEXT[0]:
                    fileTyp = 'mayaAscii'
                    
                if TmpFileSplit[1] in listMayaEXT[1]:
                    fileTyp = 'mayaBinary'
                    
                NSName = TmpFileSplit[0]
                maFilePath = os.path.join(self.plDir, i)
                
                #import maFilePath
                cmds.file(maFilePath, i=True, typ=fileTyp, iv=True, ra=True, mnc=False, ns=NSName, op='v=0', pr=True)
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
                
                
                
                
    #Import ABCfiles
    def ImportABCfiles(self):
        listEXT = ['.abc']
        for i in os.listdir(self.plDir):
            TmpFileSplit = os.path.splitext(i)
            if TmpFileSplit[1] in listEXT:
                abcFilePath = os.path.join(self.plDir, i)
                print i
                #cmds.file(abcFilePath, i=True)
                #AbcImport -mode import -connect "-OBJTOREPLACE-" "Q:/Info5Film/Heritage/08_DIVERS/SQ01_PL51_TaylorCache.abc";
                
    #Import VDBfiles
    def ImportVDBfiles(self):
        listEXT = ['.vdb']
        for i in os.listdir(self.plDir):
            TmpFileSplit = os.path.splitext(i)
            if TmpFileSplit[1] in listEXT:
                vdbFilePath = os.path.join(self.plDir, i)
                print i
                #cmds.file(abcFilePath, i=True)
        
p = AutoAssemblyBuilder()