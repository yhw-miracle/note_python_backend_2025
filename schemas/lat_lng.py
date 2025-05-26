from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class LatLngSchema(BaseSchema):
    # 经度
    lat = fields.String(required=True)
    # 纬度
    lng = fields.String(required=True)
    # 次数
    count = fields.Integer(dump_default=1)