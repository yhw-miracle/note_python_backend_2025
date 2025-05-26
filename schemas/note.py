from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class NoteSchema(BaseSchema):
    # 笔记id
    note_id = fields.String(required=True)
    # 笔记标题
    title = fields.String(required=True)
    # 笔记内容 hash
    content_hash = fields.Raw(required=True)
    # 笔记路径
    path = fields.String(required=True)
    # 分类id
    category_id = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
    # 更新时间
    update_time = fields.Float(allow_none=True)

class GetNoteSchema(BaseSchema):
    # 笔记id
    note_id = NotEmptyString(required=True)
