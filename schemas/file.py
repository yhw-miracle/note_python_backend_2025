from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class FileSchema(BaseSchema):
    # 文件id
    file_id = fields.String(required=True)
    # 文件类型
    file_type = fields.String(allow_none=True)
    # 文件名称
    name = fields.String(required=True)
    # 文件路径
    path = fields.String(allow_none=True)
    # 创建时间
    create_time = fields.Float(required=True)

class AddFileSchema(BaseSchema):
    # 文件类型
    file_type = fields.String()
    # 文件名称
    name = NotEmptyString(required=True)
    # 文件路径
    path = fields.String()

class GetFileSchema(BaseSchema):
    # 文件id
    file_id = NotEmptyString(required=True)
