from ..database import Base

_OPTIMISTIC_LOCK_EXCLUDED_TABLES = {
    "COORDINATION_PROTOCOL_EVENT_LOG",
    "COORDINATION_TIME_LOG",
}


def _to_human_label(attr_name: str) -> str:
    """Convert attribute name to human-readable label."""
    label = attr_name.replace("_", " ").strip().title()
    label = label.replace(" Id", " ID").replace(" Nr", " Nr.")
    return label


def apply_entity_metadata_defaults() -> None:
    """Add default label/comment metadata for all mapped columns."""
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        for column in mapper.local_table.columns:
            attr_name = column.key
            if column.info is None:
                column.info = {}
            column.info.setdefault("label", _to_human_label(attr_name))
            if not column.comment:
                column.comment = f"{_to_human_label(attr_name)} ({cls.__name__})."


def _next_row_version(current_version: int | None) -> int:
    return 1 if current_version is None else current_version + 1


def apply_optimistic_locking_defaults() -> None:
    """Enable SQLAlchemy optimistic locking for mapped entities by default."""
    for mapper in Base.registry.mappers:
        table = mapper.local_table
        if table.name in _OPTIMISTIC_LOCK_EXCLUDED_TABLES:
            continue
        row_version_column = table.columns.get("ROW_VERSION")
        if row_version_column is None:
            continue
        mapper.version_id_col = row_version_column
        mapper.version_id_generator = _next_row_version
