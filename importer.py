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
        leaf = name
        name = path + "." + name
    if sys.modules.has_key(name):
        
        if hasattr(sys.modules[name],'__file__'):
            print sys.modules[name].__file__
            module_path = sys.modules[name].__file__
            if module_path[-1] == 'c':
                module_path = module_path[0:-1]
            if os.path.exists(module_path):
                if os.stat(module_path).st_mtime > os.stat(module_path + 'c').st_mtime:
                    # The module has been modified, reimport it
                    del(sys.modules[name])
                    print "###REIMPORTED###"
                    return child(__builtin__.__import__(name), leaf)
            else:
                # The module no longer exists, remove it
                del(sys.modules[name])
                print "###REMOVED###"
                return None
        # Do not reimport, simply return the unmodified module
        print "###RETURNED###"
        return sys.modules[name]
    else:
        # Initial import
        print "###INITIALLY IMPORTED###"
        return child(__builtin__.__import__(name), leaf)
