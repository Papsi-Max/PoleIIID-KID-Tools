import os
import sys
import nuke
import AComper

# AP definitions

toolbar = nuke.menu('Nodes')
AMenu = toolbar.addMenu('AComper', icon='AComper_icon.png')
AMenu.addCommand('AComper', 'AComper.start()', 'ctrl+a', icon='AComper_icon.png')