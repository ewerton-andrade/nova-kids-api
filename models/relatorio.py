from db import db

class RelatorioModel(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    relatorio= db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Relatorio {self.id}>'