from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class AboutMeSchema(BaseSchema):
    # 关于我id
    about_me_id = fields.String(required=True)
    # 内容
    content = fields.Raw(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
    # 更新时间
    update_time = fields.Float(allow_none=True)

class AddAboutMeSchema(BaseSchema):
    # 内容
    content = NotEmptyString(required=True)

class ModifyAboutMeSchema(BaseSchema):
    # 关于我id
    about_me_id = NotEmptyString(required=True)
    # 内容
    content = NotEmptyString(required=True)

class GetAboutMeSchema(BaseSchema):
    # 关于我id
    about_me_id = NotEmptyString(required=True)
