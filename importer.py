import __builtin__
import sys,os

def child(parent, name):
    if parent.__name__ != name:
        return getattr(parent, name)
    else:
        return parent

def __import__(name, glob = globals(), loc = locals(), path=""):
    """Runtime reloading importer.

    Import a module multiple times, when code has changed on disk between each import, updating the code getting executed."""
    print "###IMPORTER###"
    #if not sys.modules.has_key(path):
    #    __import__(path, glob, loc)
    if path:
        module = name
        name = path + "." + name
    if sys.modules.has_key(name):
        if hasattr(sys.modules[name],'__file__'):
            print sys.modules[name].__file__
            if os.path.exists(sys.modules[name].__file__[0:-1]):
                #del(glob[name])
                if os.stat(sys.modules[name].__file__[0:-1]).st_mtime > os.stat(sys.modules[name].__file__).st_mtime:
                    del(sys.modules[name])
                    print "###REIMPORTED###"
                    return child(__builtin__.__import__(name), module)
            else:
                del(sys.modules[name])
                print "###REMOVED###"
                return None
        print "###RETURNED###"
        return sys.modules[name]
    else:
        print "###INITIALLY IMPORTED###"
        return child(__builtin__.__import__(name), module)
