"""negative prompt

Revision ID: 7bb002df4dd2
Revises: c30a8fff348b
Create Date: 2023-11-26 12:32:22.786063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bb002df4dd2'
down_revision: Union[str, None] = 'c30a8fff348b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('generated_images', sa.Column('negative_prompt', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('generated_images', 'negative_prompt')
    # ### end Alembic commands ###