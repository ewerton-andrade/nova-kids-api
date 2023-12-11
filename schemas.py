from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profile = fields.Str(required=True)
    provider = fields.Str(required=True)

class RelatorioSchema(Schema):
    id = fields.Str(dump_only=True)
    crianca = fields.Str(required=True)
    data = fields.DateTime(required=True)
    presenca = fields.Boolean(required=True)
    motivo_presenca = fields.Str(required=True)
    meditacao = fields.Boolean(required=True)
    motivo_meditacao = fields.Str(required=True)
    versiculo = fields.Integer(required=True)
    motivo_versiculo = fields.Str(required=True)
    culto= fields.Boolean(required=True)
    motivo_culto = fields.Str(required=True)

class LogInSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)