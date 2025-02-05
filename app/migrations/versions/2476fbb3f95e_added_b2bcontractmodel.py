"""Added B2BContractModel

Revision ID: 2476fbb3f95e
Revises: c7d07c81e1c6
Create Date: 2024-10-02 09:59:27.763099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2476fbb3f95e'
down_revision: Union[str, None] = 'c7d07c81e1c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('b2b_contracts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('partner_seller_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('contract_terms', sa.Text(), nullable=False),
    sa.Column('revenue_sharing_percentage', sa.Float(), nullable=True),
    sa.Column('bulk_order_threshold', sa.Integer(), nullable=True),
    sa.Column('contract_start_date', sa.DateTime(), nullable=True),
    sa.Column('contract_end_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['partner_seller_id'], ['sellers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['sellers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_b2b_contracts_id'), 'b2b_contracts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_b2b_contracts_id'), table_name='b2b_contracts')
    op.drop_table('b2b_contracts')
    # ### end Alembic commands ###
