"""revision

Revision ID: 1d065d37b74f
Revises: a35a141f2ad5
Create Date: 2024-05-07 07:57:17.017238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d065d37b74f'
down_revision: Union[str, None] = 'a35a141f2ad5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.add_column('books', sa.Column('published_year', sa.Integer))

    # ### end Alembic commands ###



def downgrade() -> None:


    op.drop_column('books', 'published_year')

    # ### end Alembic commands ###



