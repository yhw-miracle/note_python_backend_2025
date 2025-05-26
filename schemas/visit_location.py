from schemas import BaseSchema, NotEmptyString
from marshmallow import fields


class VisitLocationSchema(BaseSchema):
    # 访问位置id
    visit_location_id = fields.String(required=True)
    # 按天统计
    day = fields.String(required=True)
    # IP
    ip = fields.String(required=True)
    # LONG类型IP地址
    long_ip = fields.String(required=True)
    # 运营商
    isp = fields.String(required=True)
    # 地区
    area = fields.String(required=True)
    # 省份编号
    region_id = fields.String(required=True)
    # 省份
    region = fields.String(required=True)
    # 城市编号
    city_id = fields.String(required=True)
    # 城市
    city = fields.String(required=True)
    # 区域编号
    district_id = fields.String(required=True)
    # 区域
    district = fields.String(required=True)
    # 国家编号
    country_id = fields.String(required=True)
    # 国家
    country = fields.String(required=True)
    # 经度
    lat = fields.String(required=True)
    # 纬度
    lng = fields.String(required=True)
    # 关联 visit_info 表
    visit_info_id = fields.String(required=True)
    # 创建时间
    create_time = fields.Float(required=True)

class AddVisitLocationSchema(BaseSchema):
    # 按天统计
    day = NotEmptyString(required=True)
    # IP
    ip = NotEmptyString(required=True)
    # LONG类型IP地址
    long_ip = NotEmptyString(required=True)
    # 运营商
    isp = NotEmptyString(required=True)
    # 地区
    area = NotEmptyString(required=True)
    # 省份编号
    region_id = NotEmptyString(required=True)
    # 省份
    region = NotEmptyString(required=True)
    # 城市编号
    city_id = NotEmptyString(required=True)
    # 城市
    city = NotEmptyString(required=True)
    # 区域编号
    district_id = NotEmptyString(required=True)
    # 区域
    district = NotEmptyString(required=True)
    # 国家编号
    country_id = NotEmptyString(required=True)
    # 国家
    country = NotEmptyString(required=True)
    # 经度
    lat = NotEmptyString(required=True)
    # 纬度
    lng = NotEmptyString(required=True)
    # 关联 visit_info 表
    visit_info_id = NotEmptyString(required=True)

class GetVisitLocationSchema(BaseSchema):
    # 访问位置id
    visit_location_id = NotEmptyString(required=True)
