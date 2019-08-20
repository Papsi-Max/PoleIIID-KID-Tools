import os
import sys
import subprocess
from sys import platform as _platform

mayapyPath = r"C:/Program Files/Autodesk/Maya2017/bin/mayapy.exe"
exporterFilepath = r"C:/Users/mboulogne/Documents/5Film/Prod/Z_ScriptsQuiFontPlaiz/_testFolder/arnoldBatchRender/arnorldBatchRender_IRL/myPyScriptForRender_IRL.py"
mayaFilesFolderPath = r"C:/Users/mboulogne/Documents/5Film/Prod/Z_ScriptsQuiFontPlaiz/_testFolder/arnoldBatchRender/ArnorldBatchRender_IRL/mayaFileFolder"


for file in os.listdir(mayaFilesFolderPath):
    print (file)
    fileFullPath = os.path.join(mayaFilesFolderPath, file)
    print (fileFullPath)
    proces = subprocess.Popen(r'"%s" %s %s' %(mayapyPath, exporterFilepath, fileFullPath))
    proces.wait()


raw_input()