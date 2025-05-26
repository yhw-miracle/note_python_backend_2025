from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class VisitInfoSchema(BaseSchema):
    # 访问信息id
    visit_info_id = fields.String(required=True)
    # 按天统计
    day = fields.String(required=True)
    # 请求url协议
    scheme = fields.String(required=True)
    # 请求url主机
    host = fields.String(required=True)
    # 请求url路径
    path = fields.String(required=True)
    # 请求方式
    method = fields.String(required=True)
    # 请求参数 路径参数
    path_params = fields.String(allow_none=True)
    # 请求参数 请求体参数
    body_params = fields.String(allow_none=True)
    # 客户端地址
    remote_addr = fields.String(required=True)
    # 客户端标识
    user_agent = fields.String(required=True)
    # 客户端cookies
    cookies = fields.String(required=True)
    # 客户端请求头
    headers = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)

class AddVisitInfoSchema(BaseSchema):
    # 按天统计
    day = NotEmptyString(required=True)
    # 请求url协议
    scheme = NotEmptyString(required=True)
    # 请求url主机
    host = NotEmptyString(required=True)
    # 请求url路径
    path = NotEmptyString(required=True)
    # 请求方式
    method = NotEmptyString(required=True)
    # 请求参数 路径参数
    path_params = fields.String()
    # 请求参数 请求体参数
    body_params = fields.String()
    # 客户端地址
    remote_addr = NotEmptyString(required=True)
    # 客户端标识
    user_agent = NotEmptyString(required=True)
    # 客户端cookies
    cookies = NotEmptyString(required=True)
    # 客户端请求头
    headers = NotEmptyString(required=True)

class GetVisitInfoSchema(BaseSchema):
    # 访问信息id
    visit_info_id = NotEmptyString(required=True)
