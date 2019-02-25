"""empty message

Revision ID: 1218f7b8a054
Revises: 
Create Date: 2019-02-24 22:47:11.624224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1218f7b8a054'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grant_applications', sa.Column('is_draft', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'grant_applications', 'funding_call', ['call_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'grant_applications', type_='foreignkey')
    op.drop_column('grant_applications', 'is_draft')
    # ### end Alembic commands ###
