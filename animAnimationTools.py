import maya.cmds as cmds
        
def whoToIKMatch():
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
    
    if whichCharacterOMValue == 'Taylor':
        IKMatchTaylor=True
        
    if whichCharacterOMValue == 'Grace':
        IKMatchGrace=True
        
def whoToFKMatch():
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
    
    if whichCharacterOMValue == 'Taylor':
        FKMatchTaylor=True
        
    if whichCharacterOMValue == 'Grace':
        FKMatchGrace=True
        
def whoToSelectAllCtrls():
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
        
    if whichCharacterOMValue == 'Taylor':
        SelectAllCtrls('SETUP_HD_Taylor:')
        
    if whichCharacterOMValue == 'Grace':
        SelectAllCtrls('SETUP_HD_Grace:')
    
def whoToKeyWall():
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
        
    if whichCharacterOMValue == 'Taylor':
        keyWall('SETUP_HD_Taylor:')
        
    if whichCharacterOMValue == 'Grace':
        keyWall('SETUP_HD_Grace:')
        
def SelectAllCtrls(whichCharacter):
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
    try:
        #Select character ctrls set
        ctrlsWhichCharacter = whichCharacter + 'set_ctrls'
        toSelect = cmds.select(ctrlsWhichCharacter)
        
    except Exception as ex:
        cmds.confirmDialog(t='Error 404 : Not found', m='Their is no ' + whichCharacterOMValue + ' in the scene.', ma='center', b='Close')


def keyWall(whichCharacter):
    whichCharacterOMValue = cmds.optionMenu('whichCharacterOM', q=1, v=1)
    try:
        #Save current selection
        savedtSel = cmds.ls(sl=1)
        #Select character ctrls set
        ctrlsWhichCharacter = whichCharacter + 'set_ctrls' 
        toSelect = cmds.select(ctrlsWhichCharacter)
        
        #List the selection
        sel = cmds.ls(sl=1)
        
        #Loop: key for sel
        for i in sel:
            cmds.setKeyframe(at='translateX')
            cmds.setKeyframe(at='translateY')
            cmds.setKeyframe(at='translateZ')
            cmds.setKeyframe(at='rotateX')
            cmds.setKeyframe(at='rotateY')
            cmds.setKeyframe(at='rotateZ')
            cmds.setKeyframe(at='IKFKSwitch')
            cmds.setKeyframe(at='footroll')
            cmds.setKeyframe(at='sideroll')
            cmds.setKeyframe(at='pivotfoot')
            cmds.setKeyframe(at='toeTap')
            cmds.setKeyframe(at='smartBlinkHeight')
            cmds.setKeyframe(at='smartBlink')
            cmds.setKeyframe(at='irisScale')
            cmds.setKeyframe(at='pupilleScale')
            
        #Deselect
        cmds.select(cl=1)
        
        #Reselect older selection
        cmds.select(savedtSel)
        
    except Exception as ex:
        cmds.confirmDialog(t='Error 404 : Not found', m='Their is no ' + whichCharacterOMValue + ' in the scene.', ma='center', b='Close')


def buildUI():
    #Windows Settings
    winTitle = "Animator Animation Tools"
    winName = "animAnimationTools"
    winWidth = 600
    if cmds.window(winName, exists=True):
      cmds.deleteUI(winName)
    cmds.window(winName, width=winWidth, title=winTitle)
    
    #UI code
    mainCL = cmds.columnLayout() 
    mainRLWidth = [winWidth*0.49, winWidth*0.01, winWidth*0.49]
    mainRL = cmds.rowLayout(w=winWidth, numberOfColumns=3, columnWidth3=mainRLWidth, rowAttach=((1, 'top', 0),(2, 'top', 0),(3, 'top', 0)))
    
    ###########################################################################################
    cmds.columnLayout(w=mainRLWidth[0]) # create a columnLayout under the first row of mainRL
    cmds.text(label='Choose on which character you are working on', font='boldLabelFont')
    cmds.text(label='')
    
    tmpRowWidth = [mainRLWidth[2]*0.045, mainRLWidth[2]*0.5, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text(label='', width=tmpRowWidth[0])
    cmds.optionMenu('whichCharacterOM', label='Character :', width=tmpRowWidth[1])
    cmds.menuItem( label='Taylor' )
    cmds.menuItem( label='Grace' )
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.separator(width=mainRLWidth[0], style='single', hr=True)
    cmds.setParent('..') # set UI pointer back under the main columnLayout
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='IK/FK Match options', font='boldLabelFont')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text(label='Left : ', align='right', width=tmpRowWidth[0])
    cmds.checkBox('leftCB', l="", en=False, width=tmpRowWidth[1]) #Disable
    cmds.text(label='Right : ', align='right', width=tmpRowWidth[2])
    cmds.checkBox('rightCB', l="", en=False, width=tmpRowWidth[3]) #Disablea
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = [mainRLWidth[0]*0.5, mainRLWidth[0]*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.button(label='IK Match', width=tmpRowWidth[0], en=False, height=70, align='center', command='whoToIKMatch()')
    cmds.button(label='FK Match', width=tmpRowWidth[1], en=False, height=70, align='center', command='whoToFKMatch()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.separator(width=mainRLWidth[0], style='single', hr=True)
    cmds.setParent('..') # set UI pointer back under the main columnLayout
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='Shortcut', font='boldLabelFont')
    cmds.setParent('..') # set UI pointer back under the main columnLayout
    
    tmpRowWidth = int(mainRLWidth[0]*1)
    cmds.rowLayout(numberOfColumns=1, columnWidth=(1,tmpRowWidth))
    cmds.text(label='')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[0]*0.5, mainRLWidth[0]*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.button(label='Select All Ctrls', width=tmpRowWidth[1], height=70, align='center', command='whoToSelectAllCtrls()')
    cmds.button(label='Key Wall', width=tmpRowWidth[1], height=70, align='center', command='whoToKeyWall()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    cmds.setParent('..') # this will exit the rowLayout back to the mainRL, same as cmds.setParent(mainRL)

    ###########################################################################################
    cmds.columnLayout(width=mainRLWidth[1]) # start another vertical layout
    cmds.separator( height=271, width=mainRLWidth[1], style='single', hr=False )
    cmds.setParent('..') # set UI pointer back under the main columnLayout

    ###########################################################################################
    cmds.columnLayout(width=mainRLWidth[2]) # start another vertical layout
    cmds.text(label='ABC Exporter options', font='boldLabelFont')
    cmds.text(label='')
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.75]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.text(label='Name : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCFName', tx='', width=tmpRowWidth[1])
    cmds.setParent('..') # also can use cmds.setParent(mainRL)

    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.45, mainRLWidth[2]*0.30]
    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
    cmds.text(label='Path : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCSPath', tx='Q:\\Info5Film\\Heritage\\05_Render\\', width=tmpRowWidth[1])
    cmds.button(label='Browse', width=tmpRowWidth[2], command='fileBrowserABCExport()')
    cmds.setParent('..') # also can use cmds.setParent(mainRL)
    
    tmpRowWidth = [mainRLWidth[2]*0.25, mainRLWidth[2]*0.1, mainRLWidth[2]*0.35, mainRLWidth[2]*0.1]
    cmds.rowLayout(numberOfColumns=4, columnWidth4=tmpRowWidth)
    cmds.text(label='Start Frame : ', align='right', width=tmpRowWidth[0])
    cmds.textField('ABCSF', tx='', width=tmpRowWidth[1])
    cmds.text(label='End Frame : ', align='right', width=tmpRowWidth[2])
    cmds.textField('ABCEF', tx='', width=tmpRowWidth[3])
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

buildUI()