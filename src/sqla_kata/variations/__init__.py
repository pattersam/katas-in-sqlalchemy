import typing as t

from sqla_kata.variations import v1_sql, v2_core, v3_orm

Variation = t.Literal["v1_sql", "v2_core", "v3_orm"]

VARIATIONS: tuple[Variation] = t.get_args(Variation)

__all__ = ["VARIATIONS", "Variation", "v1_sql", "v2_core", "v3_orm"]
