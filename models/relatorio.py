from db import db
from datetime import datetime, date
from sqlalchemy.dialects.sqlite import JSON

class RelatorioModel(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    crianca = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    presenca= db.Column(db.Boolean, default=False, nullable=False)
    motivo_presenca = db.Column(db.String(255), nullable=False)
    meditacao= db.Column(db.Boolean, default=False, nullable=False)
    motivo_meditacao = db.Column(db.String(255), nullable=False)
    versiculo= db.Column(db.Integer, nullable=False)
    motivo_versiculo = db.Column(db.String(255), nullable=False)
    culto= db.Column(db.Boolean, default=False, nullable=False)
    motivo_culto = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Relatorio {self.id}>'