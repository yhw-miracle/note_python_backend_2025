from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class FriendLinkSchema(BaseSchema):
    # 友链id
    friend_link_id = fields.String(required=True)
    # 友链名称
    name = fields.String(required=True)
    # 链接
    link = fields.String(required=True)
    # slogan
    description = fields.String(allow_none=True)
    # 创建时间
    create_time = fields.Float(required=True)
    # 更新时间
    update_time = fields.Float(allow_none=True)

class AddFriendLinkSchema(BaseSchema):
    # 友链名称
    name = NotEmptyString(required=True)
    # 链接
    link = NotEmptyString(required=True)
    # slogan
    description = fields.String()

class ModifyFriendLinkSchema(BaseSchema):
    # 友链id
    friend_link_id = NotEmptyString(required=True)
    # 友链名称
    name = NotEmptyString(required=True)
    # 链接
    link = NotEmptyString(required=True)
    # slogan
    description = fields.String()

class GetFriendLinkSchema(BaseSchema):
    # 友链id
    friend_link_id = NotEmptyString(required=True)
