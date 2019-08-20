import maya.cmds as mc

defaults = ['UI', 'shared']

def num_children(ns):
    return ns.count(':')
    
namespaces = [ns for ns in mc.namespaceInfo(lon=True, r=True) if ns not in defaults]
namespaces.sort(key=num_children, reverse=True)
for ns in namespaces:
    try:
        mc.namespace (set=ns)
        mc.delete(cmds.namespaceInfo (listOnlyDependencyNodes=True))
        mc.namespace (set=':')
        mc.namespace(force=True,rm=ns)
    except RuntimeError as e:
        pass