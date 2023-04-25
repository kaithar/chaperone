import inspect
import importlib

# This module contains patches to Python.  A patch wouldn't appear here if it didn't have major impact,
# and they are constructed and researched carefully.  Avoid if possible, please.

# Patch routine for patching classes.  Ignore ALL exceptions, since there could be any number of
# reasons why a distribution may not allow such patching (though most do).  Exact code is compared,
# so there is little chance of an error in deciding if the patch is relevant.

def PATCH_CLASS(module, clsname, member, oldstr, newfunc):
    try:
        cls = getattr(importlib.import_module(module), clsname)
        should_be = ''.join(inspect.getsourcelines(getattr(cls, member))[0])
        if should_be == oldstr:
            setattr(cls, member, newfunc)
    except Exception:
        pass
