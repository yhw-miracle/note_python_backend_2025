import os
import json
import requests
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import create_session
from utils import get_sqlite_prefix, work_dir, get_hash_token
from models.category import CategoryModel
from models.note import NoteModel
from models.file import FileModel
from models.tag import TagModel
from models.tag_note import TagNoteModel
from models.file_note import FileNoteModel
from models.comment import CommentModel
from models.user import UserModel
from models.about_me import AboutMeModel
from models.friend_link import FriendLinkModel
from models.visitor import VisitInfoModel, VisitLocationModel
from models import sqlalchemy_obj
from sqlalchemy import Integer, Text, Column, Select
from datetime import datetime, timedelta
from schemas import BaseSchema
from marshmallow import fields
from tqdm import tqdm
from log import logger
from schemas.visit_info import VisitInfoSchema
from schemas.visit_location import VisitLocationSchema


class ConnectInfo(sqlalchemy_obj.Model):
    __bind_key__ = ""
    __tablename__ = "connect_info"

    id = Column("id", Integer, primary_key=True)
    host = Column("host", Text(100))
    path = Column("path", Text(1000), nullable=True)
    method = Column("method", Text(100), nullable=True)
    remote_addr = Column("remote_addr", Text(1000), nullable=True)
    user_agent = Column("user_agent", Text(1000), nullable=True)
    cookies = Column("cookies", Text(1000), nullable=True)
    headers = Column("headers", Text(1000), nullable=True)
    create_time = Column("create_time", Text(100), default=datetime.now().strftime("%Y%m%d"))

    def __repr__(self) -> str:
        return f"{self.host}_{self.create_time}"
    
class ConnectInfoSchema(BaseSchema):
    id = fields.String(required=True)
    host = fields.String(required=True)
    path = fields.String(required=True)
    method = fields.String(required=True)
    remote_addr = fields.String(required=True)
    user_agent = fields.String(required=True)
    cookies = fields.String(required=True)
    headers = fields.String(required=True)
    create_time = fields.String(required=True)

def get_ip_location(ip):
    IP_LOCATION = {
        "HOST": "https://c2ba.api.huachen.cn",
        "PATH": "/ip",
        "APPCODE": "4e03e1811fc8436183ca42f77af65dd4",
        "QUERYS": "ip="
    }
    
    url = f'{IP_LOCATION["HOST"]}{IP_LOCATION["PATH"]}?{IP_LOCATION["QUERYS"]}{ip}'
    response = requests.get(url=url, headers={"Authorization": "APPCODE "+IP_LOCATION["APPCODE"]})
    if response.status_code == 200:
        content = response.content
        ip_location_info = json.loads(content)
        if ip_location_info["ret"] == 200 and "data" in ip_location_info:
            logger.info(f"{ip} => {ip_location_info}")
            return ip_location_info["data"]
        else:
            logger.error(f"{ip} => {ip_location_info}")
    else:
        logger.error(f"{ip} => {response.status_code}")

def create_tables(db_filepath, db_engine, db_session, data_models):
    if os.path.exists(db_filepath) is False:
        for index, data_model in enumerate(data_models):
            table_name = data_model.__tablename__
            if table_name not in inspect(db_engine).get_table_names():
                create_table_sql = text(str(CreateTable(data_model.__table__)))
                db_session.execute(create_table_sql)

def connect_info_v1_visit_info_v2():
    visit_info_db_dir_v2 = os.path.join(os.getcwd(), "data_v1", "visit_info_db_old")
    visit_info_db_dir = os.path.join(os.getcwd(), "data", "visit_info_db")
    os.makedirs(visit_info_db_dir, exist_ok=True)

    for filename in tqdm(sorted(os.listdir(visit_info_db_dir_v2), key=lambda x:int(x.split(".")[0]))):
        old_db_filepath = os.path.join(visit_info_db_dir_v2, filename)
        old_db_engine = create_engine(f'{get_sqlite_prefix()}{old_db_filepath}')
        old_db_session = create_session(bind=old_db_engine)
        old_db_select_expression = Select(ConnectInfo)
        old_db_info = old_db_session.execute(old_db_select_expression).scalars().all()
        connect_info_schema = ConnectInfoSchema(many=True)
        old_db_result = connect_info_schema.dump(old_db_info)

        new_db_filepath = os.path.join(visit_info_db_dir, filename)
        new_db_engine = create_engine(f"{get_sqlite_prefix()}{new_db_filepath}")
        new_db_session = create_session(bind=new_db_engine)
        create_tables(new_db_filepath, new_db_engine, new_db_session, data_models=[VisitInfoModel, VisitLocationModel])
        day, _ = filename.split(".")

        note_db_filepath = os.path.join(os.getcwd(), "data", "note.db")
        note_db_engine = create_engine(f"{get_sqlite_prefix()}{note_db_filepath}")
        note_db_session = create_session(bind=note_db_engine)
        create_tables(note_db_filepath, note_db_engine, note_db_session, data_models=[CategoryModel, NoteModel, FileModel, TagModel, TagNoteModel, FileNoteModel, CommentModel, UserModel, AboutMeModel, FriendLinkModel, VisitInfoModel, VisitLocationModel])

        for old_db_result_item in old_db_result:
            old_id = old_db_result_item["id"]
            host = old_db_result_item["host"]
            path = old_db_result_item["path"]
            method = old_db_result_item["method"]
            remote_addr = old_db_result_item["remote_addr"]
            user_agent = old_db_result_item["user_agent"]
            cookies = old_db_result_item["cookies"]
            headers = old_db_result_item["headers"]
            create_time = old_db_result_item["create_time"]
            create_time = datetime.strptime(create_time, "%Y%m%d%H%M%S").timestamp()

            visit_info_id = get_hash_token(f"{day}_{remote_addr}_{create_time}_{old_id}")
            new_visit_info = VisitInfoModel(
                visit_info_id=visit_info_id, 
                day=day, 
                scheme="http",
                host=host, 
                path=path, 
                method=method,  
                remote_addr=remote_addr, 
                user_agent=user_agent, 
                cookies=cookies, 
                headers=headers,
                create_time=create_time
            )
            new_db_session.add(new_visit_info)
            new_db_session.commit()

            new_visit_info_for_note_db = VisitInfoModel(
                visit_info_id=visit_info_id, 
                day=day, 
                scheme="http",
                host=host, 
                path=path, 
                method=method,  
                remote_addr=remote_addr, 
                user_agent=user_agent, 
                cookies=cookies, 
                headers=headers,
                create_time=create_time
            )
            note_db_session.add(new_visit_info_for_note_db)
            note_db_session.commit()

# 新增访问信息
def add_visit_location(update_yesterday_data=False):
    work_dir = os.path.join(os.getcwd(), "data")
    visit_info_db_dir = os.path.join(work_dir, "visit_info_db")

    note_db_filepath = os.path.join(os.getcwd(), "data", "note.db")
    note_db_engine = create_engine(f"{get_sqlite_prefix()}{note_db_filepath}")
    note_db_session = create_session(bind=note_db_engine)

    now_datetime = datetime.now()
    yesterday = (now_datetime - timedelta(days=1)).strftime("%Y%m%d")

    for filename in tqdm(sorted(os.listdir(visit_info_db_dir), key=lambda x:int(x.split(".")[0]))):
        day, _ = filename.split(".")
        if update_yesterday_data is True and day != yesterday:
            continue

        visit_info_db_filepath = os.path.join(visit_info_db_dir, filename)
        visit_info_db_engine = create_engine(f'{get_sqlite_prefix()}{visit_info_db_filepath}')
        visit_info_db_session = create_session(bind=visit_info_db_engine)
        visit_info_select_expression = Select(VisitInfoModel)
        if update_yesterday_data is True:
            visit_info_model_select_expression = visit_info_model_select_expression.filter(VisitInfoModel.day == yesterday)
        visit_info = visit_info_db_session.execute(visit_info_select_expression).scalars().all()
        visit_info_schema = VisitInfoSchema(many=True)
        visit_result = visit_info_schema.dump(visit_info)

        for visit_result_item in visit_result:
            remote_addr = visit_result_item["remote_addr"]
            day = visit_result_item["day"]
            visit_info_id = visit_result_item["visit_info_id"]

            visit_location_model_select_expression = Select(VisitLocationModel).filter(VisitLocationModel.day == day, VisitLocationModel.ip == remote_addr)
            is_exist_visit_location_info = note_db_session.execute(visit_location_model_select_expression).scalars().all()
            if len(is_exist_visit_location_info) == 0:

                ip_location_info = get_ip_location(remote_addr)
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
                logger.error(f"访问信息 {day}=>{ip} 的位置信息已存在!")

def visit_info_v2_tovisit_info_v3():
    note_db_filepath = os.path.join(os.getcwd(), "data", "note.db")
    os.makedirs(os.path.dirname(note_db_filepath), exist_ok=True)
    note_db_engine = create_engine(f"{get_sqlite_prefix()}{note_db_filepath}")
    note_db_session = create_session(bind=note_db_engine)
    create_tables(note_db_filepath, note_db_engine, note_db_session, data_models=[CategoryModel, NoteModel, FileModel, TagModel, TagNoteModel, FileNoteModel, CommentModel, UserModel, AboutMeModel, FriendLinkModel, VisitInfoModel, VisitLocationModel])
    
    visit_info_v2_db_dir = os.path.join(os.getcwd(), "data_v2", "visit_info_db")
    visit_info_db_dir = os.path.join(os.getcwd(), "data", "visit_info_db")
    os.makedirs(visit_info_db_dir, exist_ok=True)
    for filename in tqdm(iterable=sorted(os.listdir(visit_info_v2_db_dir), key=lambda x:int(x.split(".")[0])), desc="filename"):
        visit_info_db_filepath = os.path.join(visit_info_db_dir, filename)
        visit_info_db_engine = create_engine(f'{get_sqlite_prefix()}{visit_info_db_filepath}')
        visit_info_db_session = create_session(bind=visit_info_db_engine)
        create_tables(visit_info_db_filepath, visit_info_db_engine, visit_info_db_session, data_models=[VisitInfoModel, VisitLocationModel])

        visit_info_v2_db_filepath = os.path.join(visit_info_v2_db_dir, filename)
        visit_info_v2_db_engine = create_engine(f'{get_sqlite_prefix()}{visit_info_v2_db_filepath}')
        visit_info_v2_db_session = create_session(bind=visit_info_v2_db_engine)
        columns_name = [_["name"] for _ in inspect(visit_info_v2_db_engine).get_columns("visit_info")]
        if "scheme" not in columns_name:
            visit_info_v2_db_session.execute(text("alter table visit_info add column scheme VARCHAR(256) not null default http;"))
            visit_info_v2_db_session.commit()

        visit_info_v2_db_select_expression = Select(VisitInfoModel)
        visit_info_v2_db_info = visit_info_v2_db_session.execute(visit_info_v2_db_select_expression).scalars().all()
        visit_info_schema = VisitInfoSchema(many=True)
        visit_info_v2_db_result = visit_info_schema.dump(visit_info_v2_db_info)
        for visit_info_v2_db_result_item in tqdm(iterable=visit_info_v2_db_result, desc=f"visit_info_{filename}"):
            new_visit_info = VisitInfoModel(
                visit_info_id=visit_info_v2_db_result_item["visit_info_id"], 
                day=visit_info_v2_db_result_item["day"], 
                scheme="http", 
                host=visit_info_v2_db_result_item["host"], 
                path=visit_info_v2_db_result_item["path"], 
                method=visit_info_v2_db_result_item["method"],  
                remote_addr=visit_info_v2_db_result_item["remote_addr"], 
                user_agent=visit_info_v2_db_result_item["user_agent"], 
                cookies=visit_info_v2_db_result_item["cookies"], 
                headers=visit_info_v2_db_result_item["headers"],
                create_time=visit_info_v2_db_result_item["create_time"]
            )
            visit_info_db_session.add(new_visit_info)
            visit_info_db_session.commit()

            new_visit_info_for_note_db = VisitInfoModel(
                visit_info_id=visit_info_v2_db_result_item["visit_info_id"], 
                day=visit_info_v2_db_result_item["day"], 
                scheme="http", 
                host=visit_info_v2_db_result_item["host"], 
                path=visit_info_v2_db_result_item["path"], 
                method=visit_info_v2_db_result_item["method"],  
                remote_addr=visit_info_v2_db_result_item["remote_addr"], 
                user_agent=visit_info_v2_db_result_item["user_agent"], 
                cookies=visit_info_v2_db_result_item["cookies"], 
                headers=visit_info_v2_db_result_item["headers"],
                create_time=visit_info_v2_db_result_item["create_time"]
            )
            note_db_session.add(new_visit_info_for_note_db)
            note_db_session.commit()

        visit_localtion_v2_db_select_expression = Select(VisitLocationModel)
        visit_localtion_v2_db_info = visit_info_v2_db_session.execute(visit_localtion_v2_db_select_expression).scalars().all()
        visit_localtion_schema = VisitLocationSchema(many=True)
        visit_localtion_v2_db_result = visit_localtion_schema.dump(visit_localtion_v2_db_info)
        for visit_localtion_v2_db_result_item in tqdm(iterable=visit_localtion_v2_db_result, desc=f"visit_localtion_{filename}"):
            new_visit_location_for_visit_info_db = VisitLocationModel(
                visit_location_id=visit_localtion_v2_db_result_item["visit_location_id"], 
                day=visit_localtion_v2_db_result_item["day"], 
                ip=visit_localtion_v2_db_result_item["ip"], 
                long_ip=visit_localtion_v2_db_result_item["long_ip"], 
                isp=visit_localtion_v2_db_result_item["isp"], 
                area=visit_localtion_v2_db_result_item["area"], 
                region_id=visit_localtion_v2_db_result_item["region_id"], 
                region=visit_localtion_v2_db_result_item["region"], 
                city_id=visit_localtion_v2_db_result_item["city_id"], 
                city=visit_localtion_v2_db_result_item["city"], 
                district_id=visit_localtion_v2_db_result_item["district_id"],
                district=visit_localtion_v2_db_result_item["district"],
                country_id=visit_localtion_v2_db_result_item["country_id"],
                country=visit_localtion_v2_db_result_item["country"],
                lat=visit_localtion_v2_db_result_item["lat"],
                lng=visit_localtion_v2_db_result_item["lng"],
                visit_info_id=visit_localtion_v2_db_result_item["visit_info_id"],
                create_time=visit_localtion_v2_db_result_item["create_time"]
            )
            visit_info_db_session.add(new_visit_location_for_visit_info_db)
            visit_info_db_session.commit()

            new_visit_location = VisitLocationModel(
                visit_location_id=visit_localtion_v2_db_result_item["visit_location_id"], 
                day=visit_localtion_v2_db_result_item["day"], 
                ip=visit_localtion_v2_db_result_item["ip"], 
                long_ip=visit_localtion_v2_db_result_item["long_ip"], 
                isp=visit_localtion_v2_db_result_item["isp"], 
                area=visit_localtion_v2_db_result_item["area"], 
                region_id=visit_localtion_v2_db_result_item["region_id"], 
                region=visit_localtion_v2_db_result_item["region"], 
                city_id=visit_localtion_v2_db_result_item["city_id"], 
                city=visit_localtion_v2_db_result_item["city"], 
                district_id=visit_localtion_v2_db_result_item["district_id"],
                district=visit_localtion_v2_db_result_item["district"],
                country_id=visit_localtion_v2_db_result_item["country_id"],
                country=visit_localtion_v2_db_result_item["country"],
                lat=visit_localtion_v2_db_result_item["lat"],
                lng=visit_localtion_v2_db_result_item["lng"],
                visit_info_id=visit_localtion_v2_db_result_item["visit_info_id"],
                create_time=visit_localtion_v2_db_result_item["create_time"]
            )
            note_db_session.add(new_visit_location)
            note_db_session.commit()

if __name__ == "__main__":
    pass
    # connect_info_v1_visit_info_v2()
    # add_visit_location()
    # visit_info_v2_tovisit_info_v3()
