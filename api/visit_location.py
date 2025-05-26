import requests
import os
import json
from flask import Blueprint, jsonify, current_app, request
from models import get_note_db_session, get_visit_info_db_session
from sqlalchemy import Select
from models.visitor import VisitInfoModel, VisitLocationModel
from schemas.visit_info import VisitInfoSchema
from schemas.visit_location import VisitLocationSchema
from schemas.lat_lng import LatLngSchema
from utils import get_hash_token, get_sqlite_prefix
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session


visit_location_api = Blueprint("visit_location_api",  "note")

def get_ip_location(ip):
    url = f'{current_app["IP_LOCATION"]["HOST"]}{current_app["IP_LOCATION"]["PATH"]}?{current_app["IP_LOCATION"]["QUERYS"]}{ip}'
    response = requests.get(url=url, headers={"Authorization": "APPCODE "+current_app["IP_LOCATION"]["APPCODE"]})
    if response.status_code == 200:
        content = response.content
        ip_location_info = json.loads(content)
        if ip_location_info["ret"] == 200 and "data" in ip_location_info:
            current_app.logger.info(f"{ip} => {ip_location_info}")
            return ip_location_info["data"]
        else:
            current_app.logger.error(f"{ip} => {ip_location_info}")
    else:
        current_app.logger.error(f"{ip} => {response.status_code}")

# 新增访问信息
def add_visit_location():
    now_datetime = datetime.now()
    yesterday = (now_datetime - timedelta(days=1)).strftime("%Y%m%d")

    visit_info_model_select_expression = Select(VisitInfoModel).filter(VisitInfoModel.day == yesterday)
    note_db_session = get_note_db_session()
    yesterday_visit_info = note_db_session.execute(visit_info_model_select_expression).scalars().all()
    visit_info_schema = VisitInfoSchema(many=True)
    yesterday_visit_result = visit_info_schema.dump(yesterday_visit_info)

    for yesterday_visit_result_item in yesterday_visit_result:
        ip = yesterday_visit_result_item["ip"]
        day = yesterday_visit_result_item["day"]
        visit_info_id = yesterday_visit_result_item["visit_info_id"]

        visit_location_model_select_expression = Select(VisitLocationModel).filter(VisitLocationModel.day == day, VisitLocationModel.ip == ip)
        is_exist_visit_location_info = note_db_session.execute(visit_location_model_select_expression).scalars().all()
        if len(is_exist_visit_location_info) == 0:

            ip_location_info = get_ip_location(ip)
            # IP
            ip = ip_location_info["ip"]
            # LONG类型IP地址
            long_ip = ip_location_info["long_ip"]
            # ISP 运营商
            isp = ip_location_info["isp"]
            # area 地区
            area = ip_location_info["area"]
            # 省份编号
            region_id = ip_location_info["region_id"]
            # 省份
            region = ip_location_info["region"]
            # 城市编号
            city_id = ip_location_info["city_id"]
            # 城市
            city = ip_location_info["city"]
            # 区域编号
            district_id = ip_location_info["district_id"]
            # 区域
            district = ip_location_info["district"]
            # 国家编号
            country_id = ip_location_info["country_id"]
            # 国家
            country = ip_location_info["country"]
            # 经度
            lat = ip_location_info["lat"]
            # 纬度
            lng = ip_location_info["lng"]

            visit_info_db_session = get_visit_info_db_session()
        
            create_time = now_datetime.timestamp()
            visit_location_id = get_hash_token(f"{visit_info_id}_{day}_{ip}_{create_time}")

            new_visit_location_for_visit_info_db = VisitLocationModel(
                visit_location_id=visit_location_id, 
                day=day, 
                ip=ip, 
                long_ip=long_ip, 
                isp=isp, 
                area=area, 
                region_id=region_id, 
                region=region, 
                city_id=city_id, 
                city=city, 
                district_id=district_id,
                district=district,
                country_id=country_id,
                country=country,
                lat=lat,
                lng=lng,
                visit_info_id=visit_info_id,
                create_time=create_time
            )
            visit_info_db_session.add(new_visit_location_for_visit_info_db)
            visit_info_db_session.commit()

            new_visit_location = VisitLocationModel(
                visit_location_id=visit_location_id, 
                day=day, 
                ip=ip, 
                long_ip=long_ip, 
                isp=isp, 
                area=area, 
                region_id=region_id, 
                region=region, 
                city_id=city_id, 
                city=city, 
                district_id=district_id,
                district=district,
                country_id=country_id,
                country=country,
                lat=lat,
                lng=lng,
                visit_info_id=visit_info_id,
                create_time=create_time
            )
            note_db_session.add(new_visit_location)
            note_db_session.commit()
        else:
            current_app.logger.error(f"访问信息 {day}=>{ip} 的位置信息已存在!")

@visit_location_api.route("/sum", methods=["POST"])
def get_visit_location_sum():
    note_db_session = get_note_db_session()
    visit_info_model_select_expression = Select(VisitInfoModel)
    visit_info_info = note_db_session.execute(visit_info_model_select_expression).scalars().all()
    total_visit = len(visit_info_info)
    visit_location_model_select_group_by_country_id_expression = Select(VisitLocationModel).group_by(VisitLocationModel.country_id)
    visit_location_info_by_country_id = note_db_session.execute(visit_location_model_select_group_by_country_id_expression).scalars().all()
    total_country = len(visit_location_info_by_country_id)
    visit_location_model_select_group_by_city_id_expression = Select(VisitLocationModel).group_by(VisitLocationModel.city_id)
    visit_location_info_by_city_id = note_db_session.execute(visit_location_model_select_group_by_city_id_expression).scalars().all()
    total_city = len(visit_location_info_by_city_id)
    print(f"{type(total_visit)} --- {type(total_country)} --- {type(total_city)}")
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": {
            "total_visit": total_visit,
            "total_country": total_country,
            "total_city": total_city
        }
    })

@visit_location_api.route("/day", methods=["POST"])
def get_visit_location_day():
    result = dict()
    note_db_session = get_note_db_session()
    visit_localtion_info_model_select_expression = Select(VisitLocationModel).group_by(VisitLocationModel.day).order_by(VisitLocationModel.day.desc())
    visit_localtion_info_info = note_db_session.execute(visit_localtion_info_model_select_expression).scalars().all()
    visit_localtion_info_schema = VisitInfoSchema(many=True)
    visit_localtion_info_result = visit_localtion_info_schema.dump(visit_localtion_info_info)
    for visit_localtion_info_result_item in visit_localtion_info_result:
        day = datetime.strptime(visit_localtion_info_result_item["day"], "%Y%m%d").strftime("%Y-%m-%d")
        day_visit_localtion_info_model_select_expression = Select(VisitLocationModel).filter(VisitLocationModel.day == visit_localtion_info_result_item["day"])
        day_visit_localtion_info_info = note_db_session.execute(day_visit_localtion_info_model_select_expression).scalars().all()
        lat_lng_schema = LatLngSchema(many=True)
        day_visit_location_result = lat_lng_schema.dump(day_visit_localtion_info_info)
        if len(day_visit_location_result) > 0:
            result[day] = day_visit_location_result
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": result
    })

    # now_datetime = datetime.now()
    # token = now_datetime.strftime("%Y%m%d")
    # day_visit_info_db_result = dict()
    # day_visit_info_db_filepath = os.path.join(current_app.config["DATA"]["VISIT_INFO_DB_FOLDER"], f'{token}.db')
    # if os.path.exists(day_visit_info_db_filepath):
    #     day_visit_info_db_engine = create_engine(f'{get_sqlite_prefix()}{day_visit_info_db_filepath}')
    #     day_visit_info_db_session = create_session(bind=day_visit_info_db_engine)

    #     day_visit_info_db_select_expression = Select(VisitLocationModel)
    #     day_visit_info_db_info = day_visit_info_db_session.execute(day_visit_info_db_select_expression).scalars().all()
    #     visit_localtion_schema = VisitLocationSchema(many=True)
    #     day_visit_info_db_result = visit_localtion_schema.dump(day_visit_info_db_info)

    # return jsonify({
    #     "code": 200,
    #     "msg": "ok",
    #     "result": day_visit_info_db_result
    # })
