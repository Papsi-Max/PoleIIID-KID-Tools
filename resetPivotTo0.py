import maya.cmds as cmds

def resetPivotTo0():
    selection = cmds.ls(sl=True)
    
    for i in selection:
        cmds.makeIdentity(t=1, r=1, s=1, n=0)
        
resetPivotTo0()