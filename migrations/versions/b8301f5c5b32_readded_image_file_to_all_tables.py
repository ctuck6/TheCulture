"""Readded image_file to all tables

Revision ID: b8301f5c5b32
Revises: 99106e5d2ecc
Create Date: 2019-04-26 10:10:09.474496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8301f5c5b32'
down_revision = '99106e5d2ecc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('image_file', sa.String(length=150), nullable=True))
    op.add_column('company', sa.Column('image_file', sa.String(length=150), nullable=True))
    op.add_column('product', sa.Column('image_file', sa.String(length=150), nullable=True))
    op.add_column('user', sa.Column('image_file', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_file')
    op.drop_column('product', 'image_file')
    op.drop_column('company', 'image_file')
    op.drop_column('article', 'image_file')
    # ### end Alembic commands ###
