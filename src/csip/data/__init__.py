"""CSIP Data Module.

Provides loaders, validators, downcasters, and data profiling routines.
Complies with SKKNI [UK-03 Menelaah Data], [UK-04 Memvalidasi Data], and [UK-05 Menentukan Objek Data].
"""

from csip.data.loader import (
    OlistDataLoader,
    ValidationResult,
    downcast_dataframe,
    load_yaml_config,
)

__all__ = [
    "OlistDataLoader",
    "ValidationResult",
    "downcast_dataframe",
    "load_yaml_config",
]

