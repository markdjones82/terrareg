"""Move common submodule/moduleversion columns to new module_details table

Revision ID: 47e45e505e22
Revises: a36ffbb6580e
Create Date: 2022-07-04 16:52:55.547319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '47e45e505e22'
down_revision = 'a36ffbb6580e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('readme_content', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.Column('module_details', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('module_version', sa.Column('module_detials_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_submodule_module_details_id_module_details_id', 'module_version', 'module_details', ['module_detials_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('module_version', 'readme_content')
    op.drop_column('module_version', 'module_details')
    op.add_column('submodule', sa.Column('module_detials_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_submodule_module_details_id_module_details_id', 'submodule', 'module_details', ['module_detials_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('submodule', 'readme_content')
    op.drop_column('submodule', 'module_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submodule', sa.Column('module_details', sa.BLOB(), nullable=True))
    op.add_column('submodule', sa.Column('readme_content', sa.BLOB(), nullable=True))
    op.drop_constraint('fk_submodule_module_details_id_module_details_id', 'submodule', type_='foreignkey')
    op.drop_column('submodule', 'module_detials_id')
    op.add_column('module_version', sa.Column('module_details', sa.BLOB(), nullable=True))
    op.add_column('module_version', sa.Column('readme_content', sa.BLOB(), nullable=True))
    op.drop_constraint('fk_submodule_module_details_id_module_details_id', 'module_version', type_='foreignkey')
    op.drop_column('module_version', 'module_detials_id')
    op.drop_table('module_details')
    # ### end Alembic commands ###
