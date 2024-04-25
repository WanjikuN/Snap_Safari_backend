"""Update AlbumModel

Revision ID: 7e46abea92a1
Revises: 0af06c48e6d5
Create Date: 2024-04-24 18:11:15.818290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e46abea92a1'
down_revision: Union[str, None] = '0af06c48e6d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('albums', 'title')
    # ### end Alembic commands ###
