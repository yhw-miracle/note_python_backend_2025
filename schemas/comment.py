from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class CommentSchema(BaseSchema):
    # 评论id
    comment_id = fields.String(required=True)
    # 评论内容
    content = fields.Raw(required=True)
    # 笔记id
    note_id = fields.String(required=True)
    # 用户id
    user_id = fields.String(allow_none=True)
    # 父级评论
    parent_id = fields.String(allow_none=True)
    # 创建时间
    create_time = fields.Float(required=True)

class AddCommentSchema(BaseSchema):
    # 评论内容
    content = NotEmptyString(required=True)
    # 笔记id
    note_id = NotEmptyString(required=True)
    # 用户id
    user_id = fields.String()
    # 父级评论
    parent_id = fields.String()

class GetCommentSchema(BaseSchema):
    # 评论id
    comment_id = NotEmptyString(required=True)
