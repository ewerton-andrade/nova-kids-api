from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profile = fields.Str(required=True)
    provider = fields.Str(required=True)

class RelatorioSchema(Schema):
    id = fields.Str(dump_only=True)
    nomeCrianca = fields.Str(required=True)
    dataRelatorio = fields.DateTime(required=True)
    relatorio_presenca = fields.Dict(keys=fields.Str(), values=fields.Str())
    relatorio_meditacao = fields.Dict(keys=fields.Str(), values=fields.Str())
    relatorio_versiculo = fields.Dict(keys=fields.Str(), values=fields.Str())
    relatorio_culto = fields.Dict(keys=fields.Str(), values=fields.Str())


class LogInSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)