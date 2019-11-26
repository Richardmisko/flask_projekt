"""create users table

Revision ID: e5bf8abc7fe8
Revises: 
Create Date: 2019-11-26 12:35:04.370313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5bf8abc7fe8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
			"user",
			sa.Column("id", sa.Integer, primary_key = True),
			sa.Column("name", sa.String),
			sa.Column("password", sa.String))


def downgrade():
    op.drop_table("user")
