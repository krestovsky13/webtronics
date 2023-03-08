"""unique_posts_0002

Revision ID: d35192e3f949
Revises: 91861b204542
Create Date: 2023-03-08 17:12:31.199663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d35192e3f949"
down_revision = "91861b204542"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "post", ["title"])
    op.drop_constraint("user_username_key", "user", type_="unique")
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.create_unique_constraint("user_username_key", "user", ["username"])
    op.drop_constraint("post_title_key", "post", type_="unique")
    # ### end Alembic commands ###