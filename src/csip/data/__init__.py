"""CSIP Data Module.

Provides loaders, validators, downcasters, and data profiling routines.
Complies with SKKNI [UK-01 Menentukan Masalah Bisnis], [UK-02 Menentukan Kebutuhan Data],
[UK-03 Menelaah Data], [UK-04 Memvalidasi Data], and [UK-05 Menentukan Objek Data].
"""

from csip.data.loader import (
    OlistDataLoader,
    ValidationResult,
    downcast_dataframe,
    load_yaml_config,
)
from csip.data.semantic_profiler import (
    SEMANTIC_PATTERNS,
    build_semantic_schema,
    get_builtin_dataset,
    interpret_column_meaning,
    try_load_local_olist,
)

__all__ = [
    "OlistDataLoader",
    "ValidationResult",
    "downcast_dataframe",
    "load_yaml_config",
    "SEMANTIC_PATTERNS",
    "interpret_column_meaning",
    "build_semantic_schema",
    "try_load_local_olist",
    "get_builtin_dataset",
]
