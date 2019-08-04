"""Readded image_file to all tables

Revision ID: 447a88d982e2
Revises: 23028d45dcfe
Create Date: 2019-05-01 13:51:00.750813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447a88d982e2'
down_revision = '23028d45dcfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('image_file', sa.String(length=150), nullable=True))
    op.add_column('product', sa.Column('image_file', sa.String(length=150), nullable=True))
    op.add_column('user', sa.Column('image_file', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_file')
    op.drop_column('product', 'image_file')
    op.drop_column('company', 'image_file')
    # ### end Alembic commands ###