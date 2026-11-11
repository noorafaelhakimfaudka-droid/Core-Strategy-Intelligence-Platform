"""CSIP source root package with bidirectional import aliasing for csip and src.csip."""
import sys
import importlib.util
from pathlib import Path

_src_dir = Path(__file__).parent.resolve()
_root_dir = _src_dir.parent.resolve()

for _p in [str(_root_dir), str(_src_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

class CSIPAliasLoader:
    def __init__(self, mod):
        self.mod = mod
    def create_module(self, spec):
        return self.mod
    def exec_module(self, module):
        pass

class CSIPAliasFinder:
    def find_spec(self, fullname, path, target=None):
        if fullname == "src.csip" or fullname.startswith("src.csip."):
            alias = fullname[4:]
            try:
                __import__(alias)
                mod = sys.modules.get(alias)
                if mod:
                    return importlib.util.spec_from_loader(fullname, CSIPAliasLoader(mod))
            except Exception:
                pass
        elif fullname == "csip" or fullname.startswith("csip."):
            alias = "src." + fullname
            if alias in sys.modules:
                return importlib.util.spec_from_loader(fullname, CSIPAliasLoader(sys.modules[alias]))
        return None

if not any(isinstance(f, CSIPAliasFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, CSIPAliasFinder())

try:
    from . import csip
except Exception:
    pass
