"""empty message

Revision ID: b2a63d7095e2
Revises: 
Create Date: 2019-01-21 20:21:13.473543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2a63d7095e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('website', sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, 'company', ['website'])
    op.add_column('user', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('occupation', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('phone_number', sa.String(length=11), nullable=True))
    op.create_unique_constraint(None, 'user', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'phone_number')
    op.drop_column('user', 'occupation')
    op.drop_column('user', 'bio')
    op.drop_constraint(None, 'company', type_='unique')
    op.drop_column('company', 'website')
    # ### end Alembic commands ###