"""init

Revision ID: 98bbb05a9d6d
Revises: 
Create Date: 2023-01-18 22:48:12.761618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98bbb05a9d6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'data_stunting',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('kode_provinsi',sa.Integer,nullable=False),
        sa.Column('nama_provinsi',sa.String,nullable=False),
        sa.Column('kode_kabupaten_kota',sa.Integer,nullable=False),
        sa.Column('nama_kabupaten_kota',sa.String,nullable=False),
        sa.Column('jumlah_balita_stunting',sa.Integer,nullable=False),
        sa.Column('satuan',sa.String,nullable=False),
        sa.Column('tahun',sa.Integer,nullable=False)
    )


def downgrade():
    op.drop_table('data_stunting')
