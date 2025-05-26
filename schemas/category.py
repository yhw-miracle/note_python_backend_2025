from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class CategorySchema(BaseSchema):
    # 分类id
    category_id = fields.String(required=True)
    # 分类名称
    name = fields.String(required=True)
    # 分类描述
    description = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)
    # 更新时间
    update_time = fields.Float(allow_none=True)

class AddCategorySchema(BaseSchema):
    # 分类名称
    name = NotEmptyString(required=True)
    # 分类描述
    description = NotEmptyString(required=True)

class ModifyCategorySchema(BaseSchema):
    # 分类id
    category_id = NotEmptyString(required=True)
    # 分类名称
    name = NotEmptyString(required=True)
    # 分类描述
    description = NotEmptyString(required=True)

class GetCategorySchema(BaseSchema):
    # 分类id
    category_id = NotEmptyString(required=True)
