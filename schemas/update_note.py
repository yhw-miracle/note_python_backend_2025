from schemas import BaseSchema, NotEmptyString
from marshmallow import fields
from schemas.file import FileSchema
from schemas.tag import TagSchema, AddTagSchema


class AddNoteSchema(BaseSchema):
    # 笔记标题
    title = fields.String(required=True)
    # 笔记内容
    content = fields.String(required=True)
    # 分类id
    category_id = fields.String(required=True)
    # 笔记标签
    tags = fields.List(fields.Nested(TagSchema), load_default=list(), dump_default=list())
    # 配图 配视频
    files = fields.List(fields.Nested(FileSchema), load_default=list(), dump_default=list())

class AddNoteSchema1(BaseSchema):
    # 笔记标题
    title = fields.String(required=True)
    # 笔记内容
    content = fields.String(required=True)
    # 分类id
    category = fields.String(required=True)
    # 笔记标签
    tags = fields.List(fields.Nested(AddTagSchema), load_default=list(), dump_default=list())
    # 配图 配视频
    files = fields.List(fields.Nested(FileSchema), load_default=list(), dump_default=list())
    # 创建时间
    create_time = fields.Float()

class ModifyNoteSchema(BaseSchema):
    # 笔记id
    note_id = fields.String(required=True)
    # 笔记标题
    title = fields.String(required=True)
    # 笔记内容
    content = fields.String(required=True)
    # 分类id
    category_id = fields.String(required=True)
    # 笔记标签
    tags = fields.List(fields.Nested(TagSchema), load_default=list(), dump_default=list())
    # 配图 配视频
    files = fields.List(fields.Nested(FileSchema), load_default=list(), dump_default=list())
