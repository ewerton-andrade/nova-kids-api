from db import db
from datetime import datetime, date
from sqlalchemy.dialects.sqlite import JSON

class RelatorioModel(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    nomeCrianca = db.Column(db.String(100), nullable=False)
    dataRelatorio = db.Column(db.DateTime, default=datetime.utcnow())
    relatorio_presenca= db.Column(JSON, nullable=False)
    relatorio_meditacao= db.Column(JSON, nullable=False)
    relatorio_versiculo= db.Column(JSON, nullable=False)
    relatorio_culto= db.Column(JSON, nullable=False)

    def __repr__(self):
        return f'<Relatorio {self.id}>'