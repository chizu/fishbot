import __builtin__
import sys,os

def __import__(name):
    """Runtime reloading importer.

    Import a module multiple times, when code has changed on disk between each import, updating the code getting executed."""
    if sys.modules.has_key(name):
        if hasattr(sys.modules[name],'__file__'):
            if os.path.exists(sys.modules[name].__file__[0:-1]):
                del(sys.modules[name])
                del(globals()[name])
                if os.stat(sys.modules[name].__file__[0:-1]).st_mtime > os.stat(sys.modules[name].__file__).st_mtime:
                    print "###REIMPORTED###"
                    return __builtin__.__import__(name)
            "###REMOVED###"
            return None
        print "###RETURNED###"
        return sys.modules[name]
    else:
        print "###INITIALLY IMPORTED###"
        return __builtin__.__import__(name)
