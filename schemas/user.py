from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class UserSchema(BaseSchema):
    # 用户id
    user_id = fields.String(required=True)
    # 用户名
    username = fields.String(required=True)
    # 邮箱
    email = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)

class AddUserSchema(BaseSchema):
    # 用户名
    username = NotEmptyString(required=True)
    # 邮箱
    email = NotEmptyString(required=True)

class GetUserSchema(BaseSchema):
    # 用户id
    user_id = NotEmptyString(required=True)
