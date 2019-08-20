import maya.standalone
maya.standalone.initialize("Python")
import maya.cmds as cmds
import maya.mel as mel
import sys
sys.path.append( 'C:/solidangle/mtoadeploy/2017/scripts' )
import pymel.core as pm
import maya.app.renderSetup.views.renderSetupPreferences as prefs
import os
import getpass

mayafile = None

def renderBatch(mayaFile):
    cmds.file (mayaFile, force=True, open=True)
    importRenderPresets(mayafile)
    
def importPresetRenderSettings():
    #Variables
    user = getpass.getuser()    #Get Username
    root_src_dir = r'Q:\Info5Film\Heritage\Old_\Z_ScriptsQuiFontPlaiz\testrendersettings'    #Path/Location of the source directory
    root_dst_dir = 'C://Users//' + user + '//Documents//maya//Presets'    #Path to the destination folder
    
    #Copy/Paste render settings presets
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)
      
    
def importRenderPresets(mayafile):
    print "Trying to import renderPresets"
    #Variables
    presetToLoad = "testrendersettings"
    
    #Check Arnold load
    if not cmds.pluginInfo("mtoa", q=True, loaded=True):
        cmds.loadPlugin("mtoa")
        cmds.pluginInfo("mtoa", edit=True, autoload=True)
        
    #Set Render Using : Arnold Renderer
    cmds.setAttr('defaultRenderGlobals.ren', 'arnold', type='string')
    
    #Load Preset : testrendersettings
    prefs.loadUserPreset(presetToLoad)
    
    print "import renderPresets Done"
    #Lauch Next Step
    changeSettings(mayafile)
    
def changeSettings(mayafile):
    print "Trying to changeSettings"
    #Variables
        #Frame range
    usedStartFrame = cmds.playbackOptions(q=True,min=True)
    usedEndFrame = cmds.playbackOptions(q=True,max=True)
    
        #Prefix
    prefixtextnew = ""
    
    #Change settings
    cmds.setAttr('defaultRenderGlobals.startFrame', usedStartFrame)
    cmds.setAttr('defaultRenderGlobals.endFrame', usedEndFrame)
    cmds.setAttr('defaultRenderGlobals.imageFilePrefix', prefixtextnew, type='string')
    
    print "changeSettings Done"
    #Lauch Next Step
    createRenderFolder(mayafile)
        
def createRenderFolder(mayafile):
    print "Trying to create render folder"
    
    usedStartFrame = cmds.playbackOptions(q=True,min=True)
    usedEndFrame = cmds.playbackOptions(q=True,max=True)
    
    fF = usedStartFrame
    lF = usedEndFrame
    
    #"Q:/Info5Film/Heritage/05_Render" 
    
    path = "C:/Users/mboulogne/Documents/5Film/Prod/Z_ScriptsQuiFontPlaiz/_testFolder/arnoldBatchRender/ArnorldBatchRender_IRL/renderFileFolder" 
    
    #Create a workspace MEL file 
    workspace = '//Custom Maya Project Definition' \
                '\n' \
                'workspace -fr "images" "{}";'.format(path)
    workspace_file = r'{}\workspace.mel'.format(path)
    print workspace_file
	
    with open(workspace_file, 'w') as job_file:
        job_file.write(workspace)
    
    #Set Render  path as Maya Projects
    pm.mel.eval(r' setProject "{}"'.format(path))
    # save maya file
    pm.system.saveFile()
    
    print "Create render folder Done"
    creatBatFile(mayafile)
	
def creatBatFile(mayafile):
    renderPath = '"C:\\Program Files\\Autodesk\\Maya2017\\bin\\Render.exe"'
    filename = "C:\\Users\\mboulogne\\Documents\\5Film\\Prod\\Z_ScriptsQuiFontPlaiz\\_testFolder\\arnoldBatchRender\\ArnorldBatchRender_IRL\\renderbyscript_IRL.bat"
    
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        # Guard against race condition
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    #Open a file
    fileRender = open(filename,"w+")
    
    #Write in the file
    fileRender.write(renderPath + " " + mayafile)
    
    #Close the file
    fileRender.close()
    
    executeBatFile(mayafile)
	
def executeBatFile(mayafile):
    os.system("C:\\Windows\\System32\\cmd.exe /c C:\\Users\\mboulogne\\Documents\\5Film\\Prod\\Z_ScriptsQuiFontPlaiz\\_testFolder\\arnoldBatchRender\\ArnorldBatchRender_IRL\\renderbyscript_IRL.bat")
    
try:
    mayafile = sys.argv[1]
    print (mayafile)
    renderBatch(mayafile)
except Exception as ex:
	maya.standalone.uninitialize()
	os._exit(0);
	
maya.standalone.uninitialize()
os._exit(0);