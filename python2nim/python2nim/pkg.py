import os
import sys
import pkgutil
import importlib

package = "pytest"


# d = os.path.dirname(sys.modules[package].__file__)
# print(importlib.util.resolve_name(package, __package__))
def get_py_files(input_dir):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        for x in filenames:
            if x.endswith(".py"):
                yield os.path.join(dirpath, x)


def env_find_packages(path=None, prefix=''):
    """fuzzy search"""
    allfiles = pkgutil.walk_packages(path, prefix)
    yield from filter(lambda x: x.ispkg, allfiles)


def env_iter_modules(path=None, prefix=''):
    yield from pkgutil.iter_modules(path, prefix)

# list all submodules of ctypes
# walk_packages(ctypes.__path__, ctypes.__name__ + '.')
# @TODO
# avoid name : 'pip._internal.commands'
# avoid path : 'pip/_internal'


def module_full_path(prefix, module_name):
    """modules and sub modules"""
    return os.path.join(prefix, os.sep.join(module_name.split(".")) + ".py")


def env_files_paths():
    for p in pkgutil.walk_packages():
        yield module_full_path(p.module_finder.path, p.name)


def find_module_spec(name):
    # For illustrative purposes.
    # name = 'itertools'

    spec = importlib.util.find_spec(name)
    if spec is None:
        return
    else:
        module = importlib.util.module_from_spec(spec)
        # If you chose to perform the actual import ...
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)
        # # Adding the module to sys.modules is optional.
        # sys.modules[name] = module
