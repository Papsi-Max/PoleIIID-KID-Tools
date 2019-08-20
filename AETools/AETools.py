#................................................................................................................................................................................................

import os
import subprocess

from os.path import basename

import maya.cmds as cmds

#FrameRange Settings
defaultSF = cmds.playbackOptions(q=True,min=True)
defaultEF = cmds.playbackOptions(q=True,max=True)

#Nomdufichier
mayafile = cmds.file(q=1, sn=1)
fileNameWithExt = (basename(mayafile))
fileNameWithOutExt = os.path.splitext(fileNameWithExt)[0]

splited = fileNameWithOutExt.split("__")

if len(splited) == 4:
    fileName = splited[1] + '_' + splited[2] + '_' + splited[3]

    fileNamePlay = fileName + '_Playblast'
    fileNameABC = fileName + '_Alembic'
    
else: 
    fileNamePlay = fileNameWithOutExt
    fileNameABC = fileNameWithOutExt



#SavePath
splited = mayafile.split("__")
print splited

if len(splited) >= 4:
    defaultSavePathPlay = 'Q:\\Info5Film\\Heritage\\03_Scene\\_Animation\\__' + splited[2] + '\\___Playblast\\'
    defaultSavePathABC = 'Q:\\Info5Film\\Heritage\\03_Scene\\_Animation\\__' + splited[2] + '\\___Export_Alembic\\'
    
else:
    defaultSavePathPlay = 'Q:\\Info5Film\\Heritage\\03_Scene\\_Animation\\'
    defaultSavePathABC = 'Q:\\Info5Film\\Heritage\\03_Scene\\_Animation\\'

#Chercher ffmpeg et convertir 


def fileBrowserPlayblast():
    userSavePath = cmds.textField('playSPath', query=True, text=True)
    playPath = cmds.fileDialog2(dir=userSavePath, dialogStyle=2, fileMode=3)
    cmds.textField('playSPath', edit=True, tx=playPath[0])
    
    
def fileBrowserABCExport():
    userSavePath = cmds.textField('ABCSPath', query=True, text=True)
    abcPath = cmds.fileDialog2(dir=userSavePath, dialogStyle=2, fileMode=3)
    cmds.textField('ABCSPath', edit=True, tx=abcPath[0])


def doPlayblast():
    ffmpeg = "Q:\\Info5Film\\Heritage\\Z_Tools\\Scripts\\ffmpeg.exe"
    #Nom du playblast - OÃƒÂ¹ sauvegarder le playblast - Quelles frames rendre
    playSFrame = cmds.textField('playSF', query=True, text=True)
    playEFrame = cmds.textField('playEF', query=True, text=True)
    playSavePath = cmds.textField('playSPath', query=True, text=True)
    playFileName = cmds.textField('playFName', query=True, text=True)
    playExt = ".avi"
    playFilePath = playSavePath + '\\' + playFileName + playExt  #"C:/Users/mboulogne/Desktop/Cool2.avi" Path
    #Variables qui ne changent pas!!
    playFormat = "avi"
    playPercent = 100
    widthHeight = 1280, 720
    playClearCache = True
    viewer = False
    showOrnaments= False
    framePadding= 4
    compression= "None"
    forceOverwrite = True
    
    playExtExprot = playFileName + ".mov"
    playFilePathConvert = os.path.join(playSavePath, playExtExprot)
    
    try:
        if os.path.isfile(playFilePathConvert):
            raise ValueError('')
        else:
            cmds.playblast( fmt=playFormat, st=playSFrame, et=playEFrame, f=playFilePath, cc=playClearCache, v=viewer, orn=showOrnaments, fp=framePadding, p=playPercent, c=compression, wh=widthHeight)
            
            os.system("C:\\Windows\\System32\\cmd.exe /c" + ffmpeg+' -i '+ playFilePath + ' -vcodec libx264 ' + playFilePathConvert)
            os.remove(playFilePath)
            
            cmds.confirmDialog(t='Playblast successful', m='Your playblast has been successfuly done', b='Close')
    except Exception as ex:
        overWriting = cmds.confirmDialog( title='Overwrite', message=playFileName+playExt+' already exists.'+'\n'+'Do you want to overwrite your last playblast ?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if overWriting == 'Yes':
            cmds.playblast( fmt=playFormat, st=playSFrame, et=playEFrame, f=playFilePath, cc=playClearCache, v=viewer, orn=showOrnaments, fp=framePadding, p=playPercent, c=compression, wh=widthHeight, fo=forceOverwrite)
            
            os.system("C:\\Windows\\System32\\cmd.exe /c" + ffmpeg+' -i -y '+ playFilePath + ' -vcodec libx264 ' + playFilePathConvert)
            os.remove(playFilePath)
            
            cmds.confirmDialog(t='Playblast successful', m='Your playblast has been successfuly done', b='Close')
        else:
            cmds.confirmDialog(t='ERROR : Save playblast failed', m='Your playblast have failed.', b='Close')    
    
    
    
def checkValues():
    #Check Checkboxs
    taylorCBox = cmds.checkBox('taylorCB', query=True, v=True)
    cobraCBox = cmds.checkBox('cobraCB', query=True, v=True)
    cobraBoostCBox = cmds.checkBox('cobraBoostCB', query=True, v=True)
    dragsterCBox = cmds.checkBox('dragsterCB', query=True, v=True)
    
    graceCBox = cmds.checkBox('graceCB', query=True, v=True)
    gurkhaCBox = cmds.checkBox('gurkhaCB', query=True, v=True)
    gurkhaBoostCBox = cmds.checkBox('gurkhaBoostCB', query=True, v=True)
    monsterTruckCBox = cmds.checkBox('monsterTruckCB', query=True, v=True)
    
    lightCBox = cmds.checkBox('lightCB', query=True, v=True)
    cameraCBox = cmds.checkBox('cameraCB', query=True, v=True)
    
    #Select the child of a group
    if True not in (taylorCBox, cobraCBox, cobraBoostCBox, cobraBoostCBox, dragsterCBox, graceCBox, gurkhaCBox, gurkhaBoostCBox, monsterTruckCBox, cameraCBox, lightCBox):
        taylorCBox = True
        cobraCBox = True
        cobraBoostCBox = True
        dragsterCBox = True
        graceCBox = True
        gurkhaCBox = True
        gurkhaBoostCBox = True
        monsterTruckCBox = True
        cameraCBox = True
        
    if taylorCBox:
        try:
            tmpGrpToExport = "SETUP_HD_Taylor :" + 'GRP_Meshes_Set' 
            cmds.select(tmpGrpToExport)
            taylorText = 'Taylor'
            abcExporter(taylorText)
        except Exception as ex:
            print 'No Taylor'
    
    if cobraCBox:
        try:
            tmpGrpToExport = "SETUP_HD_Cobra :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            cobraText = 'Cobra'
            abcExporter(cobraText)
        
        except Exception as ex:
            print 'No Cobra'
    
    if cobraBoostCBox:
        try:
            tmpGrpToExport = "SETUP_HD_CobraBoost :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            cobraBoostText = 'CobraBoost'
            abcExporter(cobraBoostText)
        
        except Exception as ex:
            print 'No Cobra Boost'
    
    if dragsterCBox:
        try:
            tmpGrpToExport = "SETUP_HD_Dragster :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            dragsterText = 'Dragster'
        
        except Exception as ex:
            print 'No Dragster'
    
    if graceCBox:
        try:
            tmpGrpToExport = "SETUP_HD_Grace :" + "GRP_Meshes_Set"
            abc=True
            graceText = 'Grace'
        
        except Exception as ex:
            print 'No Grace'
    
    if gurkhaCBox:
        try:
            tmpGrpToExport = "SETUP_HD_Gurkha :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            gurkhaText = 'Gurkha'
            abcExporter(gurkhaText)
        
        except Exception as ex:
            print 'No Gurkha'
    
    if gurkhaBoostCBox:
        try:
            tmpGrpToExport = "SETUP_HD_GurkhaBoost :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            gurkhaBoostText = 'GurkhaBoost'
            abcExporter(gurkhaBoostText)
        
        except Exception as ex:
            print 'No Gurkha Boost'
    
    if monsterTruckCBox:
        try:
            tmpGrpToExport = "SETUP_HD_MonsterTruck :" + "GRP_Meshes_Set"
            cmds.select(tmpGrpToExport, hierarchy=True)
            cmds.select(tmpGrpToExport, d=True)
            monsterTruckText = 'MonsterTruck'
            abcExporter(monsterTruckText)
        
        except Exception as ex:
            print 'No Monster Truck'
            
    if lightCBox:
        try:
            tmpSetToExport = "light_Set"
            cmds.select(tmpSetToExport)
            lightExporter()
        except Exception as ex:
            print 'No Light Set'

        
    
def abcExporter(exportedName):
    #Check abcPlugins load
    if not cmds.pluginInfo("AbcExport", q=True, loaded=True):
        cmds.loadPlugin("AbcExport")
        cmds.pluginInfo("AbcExport", edit=True, autoload=True)
        cmds.pluginInfo("AbcImport", edit=True, autoload=True)
    
    
    #Nom du fichier ABC - OÃƒÂ¹ sauvegarder le fichier ABC - Quelles frames Ãƒ  exporter
    ABCSFrame = cmds.textField('ABCSF', query=True, text=True)
    ABCEFrame = cmds.textField('ABCEF', query=True, text=True)
    ABCSavePath = cmds.textField('ABCSPath', query=True, text=True) + '\\'
    ABCFileName = cmds.textField('ABCFName', query=True, text=True)
    ABCExt = ".abc"
    ABCFileName_reformat = ABCFileName + '_' + exportedName + ABCExt #Path
    ABCFilePath = os.path.join(ABCSavePath, ABCFileName_reformat)
    
    
    #Prepare the selection
    sel = cmds.ls(sl=1, l=1)
    z=""
    for i in sel:
	    z+=" -root " + i
    
    #Save the abc File
    command = "-frameRange " + str(ABCSFrame) + " " + str(ABCEFrame) + " -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa"+ z + " -file " + ABCFilePath
    cmds.AbcExport ( j = command )

def lightExporter():
    lightSavePath = cmds.textField('ABCSPath', query=True, text=True) + '\\'
    lightFileName = cmds.textField('ABCFName', query=True, text=True)
    lightExt = ".ma"
    lightFileName_reformat = lightFileName + '_' + "Light" + lightExt #Path
    lightFilePath = os.path.join(lightSavePath, lightFileName_reformat)
    
    #?file -force -options "v=0;" -typ "mayaAscii" -es "C:/Users/mboulogne/Desktop/testexportabc/maya/light_export_test_01.ma";
    cmds.file(lightFilePath, f=1, op="v=0", typ="mayaAscii", es=1)

def AETools():
    #Windows Settings
    winTitle = "Animator Export Tools"
    winName = "animExportTools"
    winWidth = 600
    if cmds.window(winName, exists=True):
      cmds.deleteUI(winName)
    cmds.window(winName, width=winWidth, title=winTitle)
    
    #UI code
    mainCL = cmds.columnLayout() 
    mainRLWidth = [winWidth*0.49, winWidth*0.01, winWidth*0.49]
    mainRL = cmds.rowLayout(w=winWidth, numberOfColumns=3, columnWidth3=mainRLWidth, rowAttach=((1, 'top', 0),(2, 'top', 0),(3, 'top', 0)))
    cmds.columnLayout(w=mainRLWidth[0]) # create a columnLayout under the first row of mainRL
    cmds.text(label='Playblast options', font='boldLabelFont')
    cmds.text(label='')
    
    tmpRowWidth = [mainRLWidth[0]*0.25, mainRLWidth[0]*0.75]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.text(label='Name : ', align='right', width=tmpRowWidth[0])
    cmds.textField('playFName', tx=fileNamePlay, width=tmpRowWidth[1])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = [mainRLWidth[0]*0.25, mainRLWidth[0]*0.45, mainRLWidth[0]*0.30]
    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
    cmds.text(label='Path : ', align='right', width=tmpRowWidth[0])
    cmds.textField('playSPath', tx=defaultSavePathPlay, width=tmpRowWidth[1])
    cmds.button(label='Browse', width=tmpRowWidth[2], command='fileBrowserPlayblast()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[0]*0.25, mainRLWidth[0]*0.1, mainRLWidth[0]*0.53, mainRLWidth[0]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text(label='Start Frame : ', align='right', width=tmpRowWidth[0])
    cmds.textField('playSF', tx=int(defaultSF), width=tmpRowWidth[1])
    cmds.text(label='End Frame : ', align='right', width=tmpRowWidth[2])
    cmds.textField('playEF', tx=int(defaultEF), width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.button(label='Launch Playblast', width=tmpRowWidth, height=70, align='center', command='doPlayblast()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    cmds.setParent('..') # this will exit the rowLayout back to the mainRL, same as cmds.setParent(mainRL)

    cmds.columnLayout(width=mainRLWidth[1]) # start another vertical layout
    cmds.separator( height=271, width=mainRLWidth[1], style='single', hr=False )
    cmds.setParent('..') # set UI pointer back under the main columnLayout

    cmds.columnLayout(width=mainRLWidth[2]) # start another vertical layout
    cmds.text(label='ABC Exporter options', font='boldLabelFont')
    cmds.text(label='')
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.75]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.text(label='Name : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCFName', tx=fileNameABC, width=tmpRowWidth[1])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.45, mainRLWidth[2]*0.30]
    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
    cmds.text(label='Path : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCSPath', tx=defaultSavePathABC, width=tmpRowWidth[1])
    cmds.button(label='Browse', width=tmpRowWidth[2], command='fileBrowserABCExport()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text(label='Start Frame : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCSF', tx=int(defaultSF), width=tmpRowWidth[1])
    cmds.text(label='End Frame : ', align='right', width=tmpRowWidth[2])
    cmds.textField('ABCEF', tx=int(defaultEF), width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[2])
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[2])
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='Check what do you want to export :', font='boldLabelFont')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text('taylorCBText', label='Taylor : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('taylorCB', l="", width=tmpRowWidth[1])
    cmds.text('graceCBText', label='Grace : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('graceCB', l="", width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text('cobraCBText', label='Cobra : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('cobraCB', l="", width=tmpRowWidth[1])
    cmds.text('gurkhaCBText', label='Gurkha : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('gurkhaCB', l="", width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text('cobraBoostCBText', label='Cobra Boost : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('cobraBoostCB', l="", width=tmpRowWidth[1])
    cmds.text('gurkhaBoostCBText', label='Gurkha Boost : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('gurkhaBoostCB', l="", width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text('dragsterCBText', label='Dragster : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('dragsterCB', l="", width=tmpRowWidth[1])
    cmds.text('monsterTruckCBText', label='Monster Truck : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('monsterTruckCB', l="", width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text('cameraCBText', label='Camera : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('cameraCB', l="", width=tmpRowWidth[1])
    cmds.text('lightCBText', label='Lights : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('lightCB', l="", width=tmpRowWidth[3])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[2])
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = int(mainRLWidth[2])
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.button(label='Launch ABC Exporter', width=tmpRowWidth, height=70, align='center', command='checkValues()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    cmds.setParent('..') # this will exit the rowLayout back to the mainRL, same as cmds.setParent(mainRL)

    cmds.setParent(mainCL) # set UI pointer back under the main columnLayout
    cmds.text(label='')
    cmds.button(label='Close', width=winWidth, height=40)

    cmds.showWindow(winName)
    cmds.window(winName, e=True, width=winWidth, height=1)
    return

AETools()