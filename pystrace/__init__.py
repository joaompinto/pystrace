from ._version import get_versions
from .tracer import Tracer

__version__ = get_versions()["version"]
del get_versions

__all__ = [Tracer, __version__]
