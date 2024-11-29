from abc import ABC
from typing import LiteralString

from psycopg import AsyncConnection
from psycopg import sql
from psycopg.abc import Query


class Migration(ABC):
    async def up(self, connection: AsyncConnection):
        raise NotImplementedError()

    async def down(self, connection: AsyncConnection):
        raise NotImplementedError()


class MigrationPlainSQL(Migration):
    def __init__(self, /, sql_up: Query, sql_down: Query):
        self.sql_up = sql_up
        self.sql_down = sql_down

    async def up(self, connection: AsyncConnection):
        await connection.execute(self.sql_up)

    async def down(self, connection: AsyncConnection):
        await connection.execute(self.sql_down)


class MigrationComposite(Migration):
    def __init__(self, /, *migrations: Migration):
        self.migrations = migrations

    def add_migration(self, migration: Migration) -> "MigrationComposite":
        self.migrations.append(migration)
        return self

    async def up(self, connection: AsyncConnection):
        for migration in self.migrations:
            await migration.up(connection)

    async def down(self, connection: AsyncConnection):
        for migration in reversed(self.migrations):
            await migration.down(connection)


def composed(*migrations: Migration) -> Migration:
    return MigrationComposite(*migrations)


def create_table(
    table: str, columns: dict[str, str] | LiteralString, /, schema: str | None = None
) -> Migration:
    columns_str = columns
    if isinstance(columns, dict):
        columns_str = ", \n".join([f"{name} {type}" for name, type in columns.items()])

    table_ref = None
    if schema:
        table_ref = sql.Identifier(schema, table)
    else:
        table_ref = sql.Identifier(table)

    create_table = sql.SQL("CREATE TABLE {table_ref} ({columns_str})").format(
        table_ref=table_ref, columns_str=sql.SQL(columns_str)
    )
    drop_table = sql.SQL("DROP TABLE {table_ref}").format(table_ref=table_ref)
    return MigrationPlainSQL(create_table, drop_table)


MIGRATION = composed(
    create_table(
        "contacts",
        """
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT
""",
    )
)
