from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(min=4, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=120))
