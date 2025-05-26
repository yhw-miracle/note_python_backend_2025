from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class TagSchema(BaseSchema):
    # 标签id
    tag_id = fields.String(required=True)
    # 标签名
    name = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
    # 更新时间
    update_time = fields.Float(allow_none=True)

class AddTagSchema(BaseSchema):
    # 标签名
    name = NotEmptyString(required=True)

class ModifyTagSchema(BaseSchema):
    # 标签id
    tag_id = NotEmptyString(required=True)
    # 标签名
    name = NotEmptyString(required=True)

class GetTagSchema(BaseSchema):
    # 标签id
    tag_id = NotEmptyString(required=True)
