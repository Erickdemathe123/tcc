"""multi variedade talhao e colheita itens

Revision ID: e2d3890ba98c
Revises: 95a2373bad69
Create Date: 2026-06-11 23:21:18.556082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d3890ba98c'
down_revision = '95a2373bad69'
branch_labels = None
depends_on = None


def upgrade():
    # Novas tabelas (IF NOT EXISTS para caso já criadas pelo db.create_all)
    conn = op.get_bind()
    tables = [r[0] for r in conn.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()]

    if 'talhao_variedades' not in tables:
        op.create_table(
            'talhao_variedades',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('talhao_id', sa.Integer(), sa.ForeignKey('talhoes.id'), nullable=False),
            sa.Column('variedade', sa.String(length=50), nullable=False),
        )

    if 'colheita_itens' not in tables:
        op.create_table(
            'colheita_itens',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('colheita_id', sa.Integer(), sa.ForeignKey('colheitas.id'), nullable=False),
            sa.Column('variedade', sa.String(length=50), nullable=False),
            sa.Column('quantidade_caixas', sa.Integer(), nullable=True),
            sa.Column('peso_por_caixa', sa.Float(), nullable=True),
            sa.Column('preco_por_caixa', sa.Float(), nullable=True),
        )

    # Migra dados existentes: cada colheita antiga vira 1 item com variedade do talhão (ou genérica)
    colheitas = conn.execute(sa.text(
        'SELECT c.id, c.talhao_id, c.quantidade_caixas, c.peso_por_caixa, c.preco_por_caixa, t.variedade '
        'FROM colheitas c JOIN talhoes t ON t.id = c.talhao_id '
        'WHERE c.quantidade_caixas IS NOT NULL AND c.quantidade_caixas > 0'
    )).fetchall()
    for row in colheitas:
        variedade = row[5] if row[5] else 'Não especificada'
        conn.execute(sa.text(
            'INSERT INTO colheita_itens (colheita_id, variedade, quantidade_caixas, peso_por_caixa, preco_por_caixa) '
            'VALUES (:cid, :var, :qtd, :peso, :preco)'
        ), {'cid': row[0], 'var': variedade, 'qtd': row[2], 'peso': row[3], 'preco': row[4]})

    # Remove colunas antigas de colheitas
    with op.batch_alter_table('colheitas', schema=None) as batch_op:
        batch_op.drop_column('preco_por_caixa')
        batch_op.drop_column('quantidade_caixas')
        batch_op.drop_column('peso_por_caixa')

    # Remove coluna variedade de talhoes (agora em talhao_variedades)
    with op.batch_alter_table('talhoes', schema=None) as batch_op:
        batch_op.drop_column('variedade')


def downgrade():
    with op.batch_alter_table('talhoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('variedade', sa.VARCHAR(length=50), nullable=True))

    with op.batch_alter_table('colheitas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('peso_por_caixa', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('quantidade_caixas', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('preco_por_caixa', sa.FLOAT(), nullable=True))

    op.drop_table('colheita_itens')
    op.drop_table('talhao_variedades')
