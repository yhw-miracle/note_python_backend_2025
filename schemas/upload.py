from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class UploadFileSchema(BaseSchema):
    # 文件名称
    name = NotEmptyString(required=True)

class UploadFileChunkSchema(BaseSchema):
    # 文件id
    file_id = NotEmptyString(required=True)
    # 文件类型
    file_type = fields.String(load_default="image")
    # 切片编号
    chunk_number = fields.Integer(required=True)
    # 总切片数
    total_chunks = fields.Integer(required=True)