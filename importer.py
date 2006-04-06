import __builtin__
import sys,os

debug = False

def child(parent, name):
    if parent.__name__ != name:
        return getattr(parent, name)
    else:
        return parent

def __import__(name, glob = globals(), loc = locals(), path=""):
    """Runtime reloading importer.

    Import a module multiple times, when code has changed on disk between each import, updating the code getting executed."""
    #if not sys.modules.has_key(path):
    #    __import__(path, glob, loc)
    if debug: print "###IMPORTER###"
    leaf = name
    if path:
        name = path + "." + name
    if sys.modules.has_key(name):
        if hasattr(sys.modules[name],'__file__'):
            if debug: print "###LOADING:" + sys.modules[name].__file__
            module_path = sys.modules[name].__file__
            if module_path[-13:] == '/__init__.pyc':
                module_path = module_path[0:-13]
            if module_path[-4:] == '.pyc':
                module_path = module_path[0:-1]
            if os.path.exists(module_path):
                if (os.path.isdir(module_path) and os.stat(module_path).st_mtime > os.stat(module_path + "/__init__.pyc").st_mtime) or not os.path.isdir(module_path) and os.stat(module_path).st_mtime > os.stat(module_path + 'c').st_mtime:
                    # The module has been modified, reimport it
                    del(sys.modules[name])
                    if debug: print "###REIMPORTED###"
                    return child(__builtin__.__import__(name), leaf)
            else:
                # The module no longer exists, remove it
                del(sys.modules[name])
                if debug: print "###REMOVED###"
                return None
        # Do not reimport, simply return the unmodified module
        if debug: print "###RETURNED###"
        return sys.modules[name]
    else:
        # Initial import
        if debug: print "###INITIALLY IMPORTED###"
        return child(__builtin__.__import__(name), leaf)
