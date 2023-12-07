from db import db
from datetime import datetime, date

class RelatorioModel(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    nomeCrianca = db.Column(db.String(100), nullable=False)
    dataRelatorio = db.Column(db.DateTime, default=datetime.utcnow())
    relatorio= db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Relatorio {self.id}>'