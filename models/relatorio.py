from db import db
from datetime import datetime, date
from sqlalchemy.dialects.sqlite import JSON
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ARRAY

class RelatorioModel(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    id_rebanho = db.Column(db.Integer, nullable=True)
    id_crianca = db.Column(db.Integer, nullable=True)
    crianca = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    presenca= db.Column(db.Boolean, default=False, nullable=False)
    motivo_presenca = db.Column(db.ARRAY(db.String(255)), nullable=True)
    meditacao= db.Column(db.Boolean, default=False, nullable=False)
    motivo_meditacao = db.Column(db.ARRAY(db.String(255)), nullable=True)
    versiculo= db.Column(db.Integer, nullable=False)
    motivo_versiculo = db.Column(db.String(255), nullable=False)
    culto= db.Column(db.Integer, default=False, nullable=False)
    motivo_culto = db.Column(db.ARRAY(db.String(255)), nullable=True)

    def __repr__(self):
        return f'<Relatorio {self.id}>'