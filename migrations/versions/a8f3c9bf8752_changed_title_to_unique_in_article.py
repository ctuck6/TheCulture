"""changed title to unique in Article

Revision ID: a8f3c9bf8752
Revises: e6404c699f5c
Create Date: 2019-02-19 21:52:49.314674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8f3c9bf8752'
down_revision = 'e6404c699f5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'article', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='unique')
    # ### end Alembic commands ###
