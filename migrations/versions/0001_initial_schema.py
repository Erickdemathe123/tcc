"""initial schema - cria todas as tabelas do zero

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('senha_hash', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'propriedades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('localizacao', sa.String(length=200), nullable=True),
        sa.Column('area_total_ha', sa.Float(), nullable=True),
        sa.Column('produtor_nome', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name='fk_propriedades_usuario_id'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'talhoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('propriedade_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('area_ha', sa.Float(), nullable=False),
        sa.Column('data_plantio', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['propriedade_id'], ['propriedades.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'talhao_variedades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('talhao_id', sa.Integer(), nullable=False),
        sa.Column('variedade', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['talhao_id'], ['talhoes.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'manejos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('talhao_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('data_manejo', sa.Date(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('responsavel', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['talhao_id'], ['talhoes.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'ocorrencias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('talhao_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('data_ocorrencia', sa.Date(), nullable=False),
        sa.Column('severidade', sa.String(length=20), nullable=False),
        sa.Column('area_afetada_ha', sa.Float(), nullable=True),
        sa.Column('tratamento_aplicado', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['talhao_id'], ['talhoes.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'colheitas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('talhao_id', sa.Integer(), nullable=False),
        sa.Column('data_colheita', sa.Date(), nullable=False),
        sa.Column('destino', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['talhao_id'], ['talhoes.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'colheita_itens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colheita_id', sa.Integer(), nullable=False),
        sa.Column('variedade', sa.String(length=50), nullable=False),
        sa.Column('quantidade_caixas', sa.Integer(), nullable=True),
        sa.Column('peso_por_caixa', sa.Float(), nullable=True),
        sa.Column('preco_por_caixa', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['colheita_id'], ['colheitas.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'custos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('talhao_id', sa.Integer(), nullable=False),
        sa.Column('data_custo', sa.Date(), nullable=False),
        sa.Column('categoria', sa.String(length=50), nullable=False),
        sa.Column('descricao', sa.String(length=200), nullable=True),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['talhao_id'], ['talhoes.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('custos')
    op.drop_table('colheita_itens')
    op.drop_table('colheitas')
    op.drop_table('ocorrencias')
    op.drop_table('manejos')
    op.drop_table('talhao_variedades')
    op.drop_table('talhoes')
    op.drop_table('propriedades')
    op.drop_table('usuarios')
