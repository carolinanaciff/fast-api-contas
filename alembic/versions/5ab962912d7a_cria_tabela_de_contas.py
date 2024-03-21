"""cria tabela de contas

Revision ID: 5ab962912d7a
Revises: 
Create Date: 2024-03-21 09:37:06.885541

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa



revision: str = '5ab962912d7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contas_pagar_receber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.String(length=50), nullable=True),
    sa.Column('valor', sa.Float(), nullable=True),
    sa.Column('tipo', sa.String(length=7), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('contas_pagar_receber')
