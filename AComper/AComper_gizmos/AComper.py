import os
import nuke
import nukescripts.panels



class ProjectManager(nukescripts.panels.PythonPanel):
    def __init__(self, rootDir='Q:\\Info5Film\\Heritage\\05_Render\\'):
        super(ProjectManager, self).__init__('ProjectManager', 'id.ProjectManager')

        self.rootDir = rootDir
        self.seq = self.pl = None

        self.write_path = ''

        seqDirs = [x for x in os.listdir(rootDir)
                       if os.path.isdir(os.path.join(rootDir, x))]
        self.seq = seqDirs[0]
        self.seqEnum = nuke.Enumeration_Knob('SEQ', 'SEQ', seqDirs)
        self.addKnob(self.seqEnum)

        self.plEnum = nuke.Enumeration_Knob('PL', 'PL', [])
        self.addKnob(self.plEnum)

        self._seqChanged()

    def _seqChanged(self):
        self.seq = self.seqEnum.value()
        seqDir = os.path.join(self.rootDir, self.seq)
        seqPlDirs = [x for x in os.listdir(seqDir)
                          if os.path.isdir(os.path.join(seqDir, x))]
        self.plEnum.setValues(seqPlDirs)
        self._plChanged()

    def _plChanged(self):
        p = self.plEnum.value()
        if p:
            self.pl = p
            self.plDir = os.path.join(self.rootDir, self.seq, p)
        else:
            self.pl = None

    def knobChanged(self, knob):
        if knob is self.seqEnum:
            self._seqChanged()
        elif knob is self.plEnum:
            self._plChanged()

    def autocomp(self):
        p = ProjectManager()
        in_files = os.listdir(self.plDir)
        objects = []
        texture_types = []
        
        for texture in in_files:
            if not texture.lower().endswith('.jpg'):
                pass
            else:
                objects.append(texture.split('_')[0])
        
                suffix_list =  texture.split('_')[1:]
                suffix_joint = '_'.join(suffix_list)
        
                texture_types.append(suffix_joint)
        
        # On supprime les duplicatats dans les listes 
        objects_dict = dict.fromkeys(objects)
        objects_unique = objects_dict.keys()
        
        texture_types_dict = dict.fromkeys(texture_types)
        texture_types_unique = texture_types_dict.keys()
        

        premult_nodes = []
        mergeOver_nodes = []
        # Pour chaque object : 
        for o, obj in enumerate(objects_unique) :
            read_nodes = []
            merge_nodes = []

            #Pour chaque texture type
            for i, tex in enumerate(texture_types_unique[:]):
                print obj + '_' + tex
                
                the_read_premult = nuke.nodes.Read()
                the_read = nuke.nodes.Unpremult()
                the_read.setInput(0, the_read_premult)
                read_nodes.append(the_read)
                
                tex_path = os.path.join(self.plDir, (obj + '_' + tex))
                
                tex_path_correct = tex_path.replace('\\', '/') # Formattage pour nuke
                        
                the_read_premult.knob("file").setValue(tex_path_correct)
                        
                if i == 1:
                    the_merge = nuke.nodes.Merge(operation='plus')
                    merge_nodes.append(the_merge)

                    the_merge.setInput(0, read_nodes[0])
                    the_merge.setInput(1, read_nodes[1])

                if i > 1:
                    the_merge = nuke.nodes.Merge(operation='plus')
                            
                    the_merge.setInput(1, read_nodes[-1])
                    the_merge.setInput(0, merge_nodes[-1])
                
                    merge_nodes.append(the_merge)

            if texture_types_unique[-1]:
                the_premult = nuke.nodes.Premult()
                the_premult.setInput(0, merge_nodes[-1])

                premult_nodes.append(the_premult)

            if o == 1:
                the_mergeOver = nuke.nodes.Merge(operation='over')
                mergeOver_nodes.append(the_mergeOver)

                the_mergeOver.setInput(0, premult_nodes[0])
                the_mergeOver.setInput(1, premult_nodes[1])

            if o > 1:
                the_mergeOver = nuke.nodes.Merge(operation='over')
                        
                the_mergeOver.setInput(1, premult_nodes[-1])
                the_mergeOver.setInput(0, mergeOver_nodes[-1])
            
                mergeOver_nodes.append(the_mergeOver)
                
            

        
        self.outDir = os.path.join('Q:\\Info5Film\\Heritage\\06_Compo\\', self.seq, self.pl, '__SHOT01')
        self.write_path = os.path.join(self.outDir, 'SHOT01.jpg')
        write_path_correct = self.write_path.replace('\\', '/')
            
        the_write = nuke.nodes.Write()
            
        the_write.knob("file").setValue(write_path_correct)
        the_write.knob("channels").setValue('rgba')
        the_write.knob("file_type").setValue('jpg')
            
        the_write.setInput(0, the_mergeOver)
    
        #nuke.execute(the_write, 1, 1)

def start():
    p = ProjectManager()
    if p.showModalDialog():
        print p.seq, p.pl, p.plDir
        p.autocomp()