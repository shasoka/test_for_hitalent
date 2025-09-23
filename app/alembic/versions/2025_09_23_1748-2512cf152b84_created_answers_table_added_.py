"""Created answers table. Added relationships and ondelete behaviour.

Revision ID: 2512cf152b84
Revises: e554e51ab8eb
Create Date: 2025-09-23 17:48:27.342081

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2512cf152b84"
down_revision: Union[str, Sequence[str], None] = "e554e51ab8eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "answers",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name=op.f("fk_answers_question_id_questions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_answers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("answers")
