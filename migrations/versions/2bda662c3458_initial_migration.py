"""Initial migration

Revision ID: 2bda662c3458
Revises: 
Create Date: 2024-09-30 17:27:04.531233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2bda662c3458'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statuses')
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('creator_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('blocked_tasks')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blocked_tasks', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
        batch_op.alter_column('creator_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)

    op.create_table('statuses',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='statuses_pkey')
    )
    # ### end Alembic commands ###
