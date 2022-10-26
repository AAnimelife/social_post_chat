"""Persons->Users

Revision ID: 5d12908ea678
Revises: 
Create Date: 2021-12-18 13:02:43.964343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d12908ea678'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Dialogues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('img_dialogue', sa.String(), nullable=True),
    sa.Column('data_dialogues', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('second_name', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('data_born', sa.String(), nullable=True),
    sa.Column('is_online', sa.Integer(), nullable=True),
    sa.Column('avatar_img', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Dialogues_table',
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('Dialogue', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Dialogue'], ['Dialogues.id'], ),
    sa.ForeignKeyConstraint(['User'], ['Users.id'], )
    )
    op.create_table('Friends_table',
    sa.Column('First_User', sa.Integer(), nullable=True),
    sa.Column('Second_User', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['First_User'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['Second_User'], ['Users.id'], )
    )
    op.create_table('Messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num_user', sa.Integer(), nullable=True),
    sa.Column('dialogue_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('date_messages', sa.String(), nullable=True),
    sa.Column('is_read', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dialogue_id'], ['Dialogues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('img_post', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_posts', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('FileM',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['Messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('FileM')
    op.drop_table('Posts')
    op.drop_table('Messages')
    op.drop_table('Friends_table')
    op.drop_table('Dialogues_table')
    op.drop_table('Users')
    op.drop_table('Dialogues')
    # ### end Alembic commands ###
