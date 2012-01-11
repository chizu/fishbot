"""Custom importing system

__import__ here works like the builtin __import__, but will destroy any implicit references to the old code in sys.modules and reload the code if it has changed on disk.

This is error prone, if a third party module executing under the same interpreter imports the module that was pulled in with this __import__, removing it from sys could have undesirable effects. Use this __import__ function with caution."""
import __builtin__
import sys,os
import imp

# Set this to True to see what kind of import operations are actually done
debug = False

def __import__(name, glob = globals(), loc = locals(), path=""):
    """Runtime reloading importer.

    Import a module multiple times, when code has changed on disk between each import, updating the code getting executed."""
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
                    return __builtin__.__import__(name, fromlist=path)
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
        return __builtin__.__import__(name, fromlist=path)
