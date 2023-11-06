import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator, CHAR


tabluate_kwargs = {
    "headers": "keys",
    "tablefmt": "rounded_grid",
    "numalign": "center",
    "stralign": "center"
}


class GUID(TypeDecorator):
    """Platform-independent UUID type."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            # For MySQL and SQLite, use CHAR(36)
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except (TypeError, ValueError):
                raise ValueError(f"The value {value} is not a valid UUID.")

        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        try:
            return uuid.UUID(value)
        except (TypeError, ValueError):

            raise ValueError(f"The value {value} is not a valid UUID.")
