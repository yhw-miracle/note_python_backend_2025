from . import ReadOnlyModel
from sqlalchemy import Column, String

class VisitInfoModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "visit_info"

    # 访问信息id
    visit_info_id = Column("visit_info_id", String(128), primary_key=True, comment="# 访问信息id")
    # 按天统计
    day = Column("day", String(256), nullable=False, default=None, comment="# 按天统计")
    # 请求url协议
    scheme = Column("scheme", String(256), nullable=False, default=None, comment="# 请求url协议")
    # 请求url主机
    host = Column("host", String(256), nullable=False, default=None, comment="# 请求url主机")
    # 请求url路径
    path = Column("path", String(256), nullable=False, default=None, comment="# 请求url路径")
    # 请求方式
    method = Column("method", String(256), nullable=False, default=None, comment="# 请求方式")
    # 请求参数 路径参数 请求体参数
    path_params = Column("path_params", String(256), nullable=True, default=None, comment="# 请求参数 路径参数")
    body_params = Column("body_params", String(256), nullable=True, default=None, comment="# 请求参数 请求体参数")
    # 客户端地址
    remote_addr = Column("remote_addr", String(256), nullable=False, default=None, comment="# 客户端地址")
    # 客户端标识
    user_agent = Column("user_agent", String(256), nullable=False, default=None, comment="# 客户端标识")
    # 客户端cookies
    cookies = Column("cookies", String(256), nullable=False, default=None, comment="# 客户端cookies")
    # 客户端请求头
    headers = Column("headers", String(256), nullable=False, default=None, comment="# 客户端请求头")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.visit_info_id}"

class VisitLocationModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "visit_location"

    # 访问位置id
    visit_location_id = Column("visit_location_id", String(128), primary_key=True, comment="# 访问位置id")
    # 按天统计
    day = Column("day", String(256), nullable=False, default=None, comment="# 按天统计")
    # IP
    ip = Column("ip", String(256), nullable=False, default=None, comment="# IP")
    # long_ip LONG类型IP地址
    long_ip = Column("long_ip", String(256), nullable=False, default=None, comment="# LONG类型IP地址")
    # ISP 运营商
    isp = Column("isp", String(256), nullable=False, default=None, comment="# 运营商")
    # area 地区
    area = Column("area", String(256), nullable=False, default=None, comment="# 地区")
    # 省份编号
    region_id = Column("region_id", String(256), nullable=False, default=None, comment="# 省份编号")
    # 省份
    region = Column("region", String(256), nullable=False, default=None, comment="# 省份")
    # 城市编号
    city_id = Column("city_id", String(256), nullable=False, default=None, comment="# 城市编号")
    # 城市
    city = Column("city", String(256), nullable=False, default=None, comment="# 城市")
    # 区域编号
    district_id = Column("district_id", String(256), nullable=False, default=None, comment="# 区域编号")
    # 区域
    district = Column("district", String(256), nullable=False, default=None, comment="# 区域")
    # 国家编号
    country_id = Column("country_id", String(256), nullable=False, default=None, comment="# 国家编号")
    # 国家
    country = Column("country", String(256), nullable=False, default=None, comment="# 国家")
    # 经度
    lat = Column("lat", String(256), nullable=False, default=None, comment="# 经度")
    # 纬度
    lng = Column("lng", String(256), nullable=False, default=None, comment="# 纬度")
    # 关联 visit_info 表
    visit_info_id = Column("visit_info_id", String(128), nullable=False, default=None, comment="# 关联 visit_info 表")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.visit_location_id}"
