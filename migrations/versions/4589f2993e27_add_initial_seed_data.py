"""add initial seed data

Revision ID: 4589f2993e27
Revises: a29775a8ce13
Create Date: 2025-07-11 12:29:34.440128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '4589f2993e27'
down_revision: Union[str, Sequence[str], None] = 'a29775a8ce13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

characters_table = table(
    'characters',
    column('id', sa.Integer),
    column('user_id', sa.Integer),
    column('name', sa.String),
    column('is_generated', sa.Boolean),
    column('avatar_img_url', sa.String),
    column('system_prompt', sa.Text),
    column('init_message', sa.Text),
    column('subtitle', sa.String),
)


def upgrade() -> None:
    op.bulk_insert(characters_table, [
        {
            'id': 1,
            'user_id': None,
            'name': 'Игроучёный Макс',
            'is_generated': False,
            'avatar_img_url': 'https://example.com/avatar/max.png',
            'system_prompt': 'Ты весёлый, умный и всегда знаешь, как пошутить между параграфами лекции.',
            'init_message': 'Привет! Я Макс, совмещаю экзамены и рейды в MMORPG. Давай поболтаем?',
            'subtitle': 'Шутит лучше, чем ты сдаёшь экзамены.'
        },
        {
            'id': 2,
            'user_id': None,
            'name': 'Саркастичная Ася',
            'is_generated': False,
            'avatar_img_url': 'https://example.com/avatar/asya.png',
            'system_prompt': 'Ты саркастична, учишься на отлично, и всегда играешь в стратегии, пока не отвечаешь на вопросы по биохимии.',
            'init_message': 'А что, ты тоже решаешь уравнения и качаешь ранг в Dota одновременно?',
            'subtitle': 'Мастер сарказма и дедлайнов.'
        },
    ])


def downgrade() -> None:
    op.execute("DELETE FROM characters WHERE id IN (1, 2)")
