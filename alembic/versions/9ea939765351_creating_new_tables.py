"""Deleting all tables

Revision ID: 9ea939765351
Revises: 2cbc237a3f88
Create Date: 2025-02-04 17:09:19.968366

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '9ea939765351'
down_revision: Union[str, None] = '2cbc237a3f88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Drops all tables from the database."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    tables = inspector.get_table_names()
    
    for table in tables:
        op.drop_table(table)
        print(f"Deleted table: {table}")

    print("All tables have been deleted.")

def downgrade() -> None:
    """No downgrade option since this deletes all tables."""
    pass
