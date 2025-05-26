from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class FileNoteSchema(BaseSchema):
    # 文件id
    file_id = fields.String(required=True)
    # 笔记id
    note_id = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
