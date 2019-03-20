"""in Product - changed default price to 0, and company nullable

Revision ID: 105204b464bc
Revises: 36c45fd0a832
Create Date: 2019-02-18 23:50:48.298839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '105204b464bc'
down_revision = '36c45fd0a832'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'company_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'company_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###