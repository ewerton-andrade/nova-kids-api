from marshmallow import Schema, fields

class RelatorioSchema(Schema):
    id = fields.Str(dump_only=True)
    id_rebanho = fields.Int(required=True)
    id_crianca = fields.Int(required=True)
    crianca = fields.Str(required=True)
    data = fields.DateTime(required=True)
    presenca = fields.Boolean(required=True)
    motivo_presenca = fields.List(fields.String(), allow_none=True, missing=[])
    meditacao = fields.Boolean(required=True)
    motivo_meditacao = fields.List(fields.String(), allow_none=True, missing=[])
    versiculo = fields.Integer(required=True)
    motivo_versiculo = fields.Str(required=True)
    culto= fields.Boolean(required=True)
    motivo_culto = fields.List(fields.String(), allow_none=True, missing=[])