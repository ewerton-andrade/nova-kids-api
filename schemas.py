from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profile = fields.Str(required=True)
    provider = fields.Str(required=True)

class RelatorioSchema(Schema):
    id = fields.Str(dump_only=True)
    relatorio = fields.Str(required=True)

class LogInSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)