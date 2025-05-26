from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class TagNoteSchema(BaseSchema):
    # 标签id
    tag_id = fields.String(required=True)
    # 笔记id
    note_id = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
